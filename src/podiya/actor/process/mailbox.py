import asyncio

from podiya.actor.message import Envelope


class MailBox:
    def __init__(self) -> None:
        self._queue = asyncio.Queue()

    def __aiter__(self):
        return self

    async def __anext__(self) -> Envelope:
        try:
            return await self._queue.get()
        except asyncio.exceptions.CancelledError:
            raise StopAsyncIteration()

    async def send(self, message: Envelope):
        self._queue.put_nowait(message)

    def terminate(self):
        self._queue.shutdown()
