from dataclasses import dataclass
from podiya.actor.genserver import GenServer
from podiya.actor.supervisor import Supervisor


class MockGenServer(GenServer):
    class Ping: ...

    @dataclass
    class Trow:
        message: str

    async def handle_call(self, payload):
        match payload:
            case MockGenServer.Ping():
                return "pong"
        return ""

    async def handle_cast(self, payload: any):
        match payload:
            case MockGenServer.Trow(message=message):
                print("Should throw exception")
                raise Exception(message)

    @staticmethod
    async def ping():
        return await MockGenServer.call(MockGenServer.Ping())

    @staticmethod
    async def trow(message):
        return await MockGenServer.cast(MockGenServer.Trow(message))


class MockSupervisor(Supervisor):
    def init(self):
        self._children = [MockGenServer()]
