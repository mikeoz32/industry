import asyncio

from podiya.actor.message import Envelope


class MailBox:
    def __init__(self) -> None:
        self._queue = asyncio.Queue()

    def __aiter__(self):
        return self

    async def __anext__(self):
        return await self._queue.get()

    async def send(self, message: Envelope):
        await self._queue.put(message)

    def terminate(self):
        self._queue.shutdown(True)
