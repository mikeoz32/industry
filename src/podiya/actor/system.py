from typing import Callable, Optional

from podiya.actor import process

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

    def spawn(self, behavior: Callable, name: str):
        """
        Spawn new process
        """

    def list(self):
        """
        Retrun list with PIDs of processes running in local node
        """

    async def __aenter__(self):
        """
        Set up kernel context
        """
        process._process_regisrty.set(process.ProcessRegistry())
        return self

    async def __aexit__(self, a, b, c): ...


async def hello():
    print("Hello")
    pid = process.self()
    print(pid)
    async for sender, message in process.receive():
        print(message)
        await process.send(sender, f"Ive got {message}")


async def hello_sync(ping: process.PID):
    print("Hello_sync")
    pid = process.self()
    print(pid)
    await process.send(ping, (pid, "Hi from pong"))
    async for message in process.receive():
        print(message)


async def main():
    async with Kernel():
        pid = process.spawn(hello)
        pid = process.spawn(hello_sync(pid))
        print(pid)
        await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(main())
