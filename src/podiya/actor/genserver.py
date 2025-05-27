import asyncio
from podiya.actor.process import call_to_name, receive, reply, send_to_name, start
from podiya.actor.system import Kernel


class GenServer:
    def __init__(self) -> None:
        pass

    async def init(self): ...

    async def handle_cast(self, payload: any):
        print("Gen Server cast")
        print(payload)

    async def handle_call(self, payload):
        return f"Got {payload}"

    async def __call__(self) -> None:
        await self.init()
        async for message in receive():
            match message.payload:
                case ("cast", payload):
                    await self.handle_cast(payload)

                case ("call", payload):
                    result = await self.handle_call(payload)
                    await reply(result, message)

    @classmethod
    def start(cls):
        return start(cls(), str(cls.__qualname__))

    @classmethod
    async def cast(cls, message):
        return await send_to_name(cls.__qualname__, ("cast", message))

    @classmethod
    async def call(cls, message):
        return await call_to_name(cls.__qualname__, ("call", message))


class TestServer(GenServer): ...


async def main():
    async with Kernel():
        TestServer.start()
        await TestServer.cast("!!!!")
        print(await TestServer.call("Some payload"))
        await asyncio.sleep(1)


asyncio.run(main())
