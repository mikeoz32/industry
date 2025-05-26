import asyncio
import inspect
import contextvars
from uuid import uuid4


class PID:
    def __init__(self) -> None:
        self._id = uuid4()
        self._address = "local"

    @property
    def address(self):
        return self._address

    @property
    def id(self):
        return self._id

    def __repr__(self) -> str:
        return f"PID<{self._id}@{self._address}>"


def behavior_to_coro(behavior):
    iscorofun = inspect.iscoroutinefunction(behavior)
    isfun = inspect.isfunction(behavior)
    if iscorofun:
        return behavior()
    elif isfun:
        return asyncio.threads.to_thread(behavior)
    elif asyncio.iscoroutine(behavior):
        return behavior
    else:
        raise ValueError("Bad behavior, should be callable or async callable")


_current_pid = contextvars.ContextVar("_current_pid")
_current_receive = contextvars.ContextVar("_current_receive")


class MailBox:
    def __init__(self) -> None:
        self._queue = asyncio.Queue()

    def __aiter__(self):
        return self

    async def __anext__(self):
        return await self._queue.get()

    async def send(self, message):
        await self._queue.put(message)


class Process:
    def __init__(self, behavior, pid: PID) -> None:
        self._behavior = behavior_to_coro(behavior)
        self._pid = pid
        self._mailbox = MailBox()

    async def __call__(self):
        _current_pid.set(self._pid)
        _current_receive.set(self._mailbox)
        await self._behavior

    async def send(self, message):
        await self._mailbox.send(message)


class ProcessRegistry:
    def __init__(self) -> None:
        self._local_processes = dict()

    def register(self, pid: PID, process: Process):
        if pid.address == "local":
            self._local_processes[pid.id] = process

    def get(self, pid: PID) -> Process:
        return self._local_processes.get(pid.id)


_process_regisrty = contextvars.ContextVar("process_registry")


def self():
    return _current_pid.get()


async def send(pid: PID, message):
    """
    Send message to process
    """
    registry = _process_regisrty.get()
    proc = registry.get(pid)
    await proc.send(message)


def receive():
    receiver = _current_receive.get()
    return receiver


def spawn(behavior):
    pid = PID()
    process = Process(behavior, pid)
    registry = _process_regisrty.get()
    registry.register(pid, process)
    asyncio.create_task(process())
    return pid
