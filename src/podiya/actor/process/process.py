import asyncio
from enum import Enum, auto
from dataclasses import dataclass
from typing import Any
from podiya.actor.message import Envelope, MessageType
from podiya.actor.process import context
from podiya.actor.process.mailbox import MailBox
from podiya.actor.process.pid import PID
from podiya.actor.utils import behavior_to_coro


class Process:
    class Status(Enum):
        Running = auto()
        Stopped = auto()

    @dataclass(frozen=True)
    class Terminate:
        """
        This message should be send to process to terminate it
        """

        reason: str | None = None

    @dataclass
    class Shutdown: ...

    @dataclass
    class Down:
        """
        Message that will be sent to monitors when process is shutted down
        """

        pid: PID
        reason: Any | None = None

    def __init__(self, behavior, pid: PID) -> None:
        self._behavior = behavior_to_coro(behavior)
        self._pid = pid
        self._mailbox = MailBox()
        self._task = None
        self._system_queue = MailBox()
        self._user_queue = MailBox()
        self._future_map = dict()
        self._monitors = set["Process"]()
        self._status = Process.Status.Stopped

    @property
    def pid(self):
        return self._pid

    @property
    def status(self):
        return self._status

    def start(self):
        self._monitor_task = asyncio.create_task(self._process_mailbox())
        self._task = asyncio.create_task(self())

    async def _process_mailbox(self):
        try:
            async for envelope in self._mailbox:
                match envelope.payload:
                    case Process.Shutdown():
                        return await self.shutdown()
                await self._process_envelope(envelope)
        except asyncio.exceptions.CancelledError:
            pass
        except BaseException as e:
            import traceback

            print(
                f"Exception in process {self.pid} - {e.__class__} - {'\n'.join(traceback.format_tb(e.__traceback__))}"
            )
        finally:
            self._status = Process.Status.Stopped

    async def _process_envelope(self, envelope: Envelope):
        if envelope.message_type == MessageType.USER:
            future: asyncio.Future = self._future_map.get(envelope.correlation_id, None)
            if future:
                future.set_result(envelope.payload)
            else:
                await self._user_queue.send(envelope)

    async def __call__(self):
        context._current_pid.set(self._pid)
        context._current_receive.set(self._user_queue)
        self._status = Process.Status.Running
        try:
            await self._behavior
        except BaseException as e:
            print(e)
            await self.shutdown(e)

    async def send(self, message):
        if self._status == Process.Status.Running:
            await self._mailbox.send(message)

    def create_future(self, correlation_id):
        future = asyncio.Future()
        self._future_map[correlation_id] = future
        return future

    def add_monitor(self, proc: "Process"):
        self._monitors.add(proc)

    def kill(self):
        self._monitor_task.cancel()
        self._task.cancel()

    async def exit(self, reason=None):
        if self._status == Process.Status.Stopped:
            return
        self._monitor_task.cancel()
        if not self._monitor_task.cancelled():
            await self._monitor_task
        self._task.cancel()
        if not self._task.cancelled():
            await self._task
        self._mailbox.terminate()
        self._user_queue.terminate()
        self._status = Process.Status.Stopped

    async def shutdown(self, reason=None):
        asyncio.create_task(self.notify_monitors(Process.Down(self.pid, reason)))
        await self.exit(reason)

    async def notify_monitors(self, message):
        # def send_to_all(monitor: "Process"):
        #     return monitor.send(message)
        #
        # return await asyncio.gather(**list(map(send_to_all, self._monitors)))
        print(f"Notifying monitors {self._monitors}")
        envelope = Envelope(self.pid, message)
        for mon in self._monitors:
            await mon.send(envelope)
