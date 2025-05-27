import asyncio
from podiya.actor.message import Envelope, MessageType
from podiya.actor.process import context
from podiya.actor.process.mailbox import MailBox
from podiya.actor.process.pid import PID
from podiya.actor.utils import behavior_to_coro


class Process:
    def __init__(self, behavior, pid: PID) -> None:
        self._behavior = behavior_to_coro(behavior)
        self._pid = pid
        self._mailbox = MailBox()
        self._task = None
        self._system_queue = MailBox()
        self._user_queue = MailBox()
        self._future_map = dict()
        self._monitors = set[PID]()

    @property
    def pid(self):
        return self._pid

    def start(self):
        self._monitor_task = asyncio.create_task(self._process_mailbox())
        self._task = asyncio.create_task(self())

    async def _process_mailbox(self):
        async for envelope in self._mailbox:
            await self._process_envelope(envelope)

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
        await self._behavior

    async def send(self, message):
        await self._mailbox.send(message)

    def create_future(self, correlation_id):
        future = asyncio.Future()
        self._future_map[correlation_id] = future
        return future

    def add_monitor(self, pid: PID):
        self._monitors.add(pid)

    def kill(self):
        self._monitor_task.cancel()
        self._task.cancel()

    def exit(self):
        self._mailbox.terminate()
