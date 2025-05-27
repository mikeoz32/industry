from enum import Enum, auto
from typing import Callable, Generic, Optional, TypeVar

from podiya.actor import process
from podiya.actor.process.pid import PID
from podiya.actor.process import call, context, receive, reply, send
from podiya.actor.process import spawn
from podiya.actor.process.registry import ProcessRegistry

import asyncio

"""
Kernel is base environment for running processes. Represents local node - one kernel is one node
"""


class Kernel:
    def __init__(
        self, node_name: Optional[str] = None, cluster_name: Optional[str] = None
    ) -> None:
        self._cluster_name = cluster_name or "default"
        self._node_name = node_name or "node-0"

    async def __aenter__(self):
        """
        Set up kernel context
        """
        context._process_regisrty.set(ProcessRegistry())
        pid = spawn(self())
        context._current_pid.set(pid)

    async def __call__(self) -> None: ...

    async def __aexit__(self, a, b, c): ...


S = TypeVar("ActorState")
B = TypeVar("ActorBehavior")


class ActorMessageType(Enum):
    CAST = auto()
    CALL = auto()


class Actor(Generic[S, B]):
    """
    Implements kind of gen server
    """

    def __init__(self, initial_state: Optional[S] = None) -> None:
        self._state = initial_state

    async def init(self): ...

    async def handle_cast(self, payload: any):
        print("Actor cast")
        print(payload)

    async def handle_call(self, payload):
        return False

    async def __call__(self) -> None:
        await self.init()
        async for message in receive():
            match message.payload:
                case (ActorMessageType.CAST, payload):
                    await self.handle_cast(payload)

                case (ActorMessageType.CALL, payload):
                    result = await self.handle_call(payload)
                    await reply(result, message)


async def hello():
    print("ping")
    pid = process.self()
    print(pid)
    async for message in process.receive():
        print("Incoming message for ping")
        print(message.payload)
        await send(message.sender, f"Ive got {message.payload}")


async def hello_sync(ping: PID):
    print("pong")
    pid = process.self()
    print(pid)
    await send(ping, "Hi from pong")
    async for message in process.receive():
        print("Incoming message for pong")
        print(message.payload)


async def server():
    async for message in receive():
        await reply(f"Reply {message.payload}", message)


async def client(server_pid: PID):
    result = await call(server_pid, "Hi from client")
    print(result)


async def main():
    async with Kernel():
        pid = spawn(hello)
        pid = spawn(hello_sync(pid))
        srv = spawn(server)
        spawn(client(srv))
        await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(main())
