import asyncio
import pytest

from podiya.actor.process import monitor, receive, self, send, spawn
from podiya.actor.process.pid import PID
from podiya.actor.process.process import Process
from podiya.actor.process.registry import find_proc

pytestmark = pytest.mark.asyncio


async def test_spawn(kernel):
    pid = spawn(lambda: 1)
    assert pid.address == "local"

    proc = find_proc(pid)
    assert pid == proc.pid

    await asyncio.sleep(0.1)

    assert proc.status == Process.Status.Running


async def test_exit_message(kernel):
    pid = spawn(lambda: 1)

    await asyncio.sleep(0.1)

    await send(pid, Process.Shutdown())

    await asyncio.sleep(0.1)

    proc = find_proc(pid)

    assert proc.status == Process.Status.Stopped


async def monitor_proc(pid_to_mon: PID, pids: list[PID], errors=[]):
    monitor(pid_to_mon)
    proc = find_proc(pid_to_mon)
    print(proc._monitors)
    assert proc._monitors == {find_proc(self())}
    async for message in receive():
        print(message)
        match message.payload:
            case Process.Down(pid=pid, reason=reason):
                pids.append(pid)
                if reason:
                    errors.append(reason)


ve = ValueError("Ha!")


async def proc_with_exception():
    async for message in receive():
        raise ve


async def test_monitor_notify(kernel):
    pids = []

    pid = spawn(lambda: 1)
    spawn(monitor_proc(pid, pids))

    await asyncio.sleep(0.1)

    await send(pid, Process.Shutdown())

    await asyncio.sleep(0.1)

    assert len(pids) == 1


async def test_catch_child_exception(kernel):
    pids = []
    errors = []
    pid = spawn(proc_with_exception)
    spawn(monitor_proc(pid, pids, errors))

    await asyncio.sleep(0.1)
    await send(pid, "")
    await asyncio.sleep(0.1)

    assert pids == [pid]
    assert errors == [ve]
