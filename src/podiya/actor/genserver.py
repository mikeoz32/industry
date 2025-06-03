import asyncio
from typing import Any
from dataclasses import dataclass
from podiya.actor.process import call_to_name, receive, reply, send_to_name, start
from podiya.actor.supervisor import ChildSpecProtocol
from podiya.actor.system import Kernel


class GenServer(ChildSpecProtocol):
    @dataclass
    class Cast:
        payload: Any

    @dataclass
    class Call:
        payload: Any

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
            print(message.payload)
            match message.payload:
                case GenServer.Cast(payload=payload):
                    await self.handle_cast(payload)

                case GenServer.Call(payload=payload):
                    result = await self.handle_call(payload)
                    await reply(result, message)

    @property
    def behavior(self):
        return self

    @property
    def name(self):
        return self.__class__.__qualname__

    @classmethod
    def start(cls):
        return start(cls(), str(cls.__qualname__))

    @classmethod
    async def cast(cls, message):
        return await send_to_name(cls.__qualname__, GenServer.Cast(message))

    @classmethod
    async def call(cls, message):
        return await call_to_name(cls.__qualname__, GenServer.Call(message))


class TestServer(GenServer): ...


# async def main():
#     async with Kernel():
#         TestServer.start()
#         await TestServer.cast("!!!!")
#         print(await TestServer.call("Some payload"))
#         await asyncio.sleep(1)
#
#
# asyncio.run(main())
