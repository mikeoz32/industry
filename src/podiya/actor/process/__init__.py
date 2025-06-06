from typing import Any, AsyncIterable, Optional
from uuid import UUID
from podiya.actor.message import Envelope
from podiya.actor.process import context
from podiya.actor.process.pid import PID
from podiya.actor.process.process import Process
from podiya.actor.process.registry import find_proc, get_process_regisrty


def register_pid(pid: PID, process: Process):
    registry = get_process_regisrty()
    registry.register(pid, process)


def register(pid: PID, name: str):
    registry = get_process_regisrty()
    registry.register_named(name, pid)


def whereis(name: str):
    registry = get_process_regisrty()
    return registry.get_named(name)


def self():
    return context._current_pid.get()


async def send(pid: PID, message: Any, correlation_id: Optional[UUID] = None):
    """
    Send message to process
    """
    proc = find_proc(pid)
    sender = self()
    envelope = Envelope(sender, message, correlation_id=correlation_id)
    await proc.send(envelope)


async def send_to_name(name: str, message: Any, correlation_id: Optional[UUID] = None):
    pid = whereis(name)
    return await send(pid, message, correlation_id)


async def call(pid: PID, message: Any):
    proc = find_proc(pid)
    caller = find_proc(self())

    envelope = Envelope(caller.pid, message)

    future = caller.create_future(envelope.correlation_id)

    await proc.send(envelope)
    print("Calling")
    return await future


async def call_to_name(name: str, message: Any):
    pid = whereis(name)
    return await call(pid, message)


async def reply(message: Any, to: Envelope):
    await send(to.sender, message, to.correlation_id)


def receive() -> AsyncIterable[Envelope]:
    receiver = context._current_receive.get()
    return receiver


def spawn(behavior) -> PID:
    pid = PID()
    process = Process(behavior, pid)
    register_pid(pid, process)
    process.start()
    return pid


def start(behavior, name):
    """
    Spawn process and registers its pid
    """
    pid = spawn(behavior)
    register(pid, name)
    return pid


def monitor(pid: PID):
    find_proc(pid).add_monitor(find_proc(self()))
