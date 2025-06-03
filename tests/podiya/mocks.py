
from podiya.actor.genserver import GenServer


class MockGenServer(GenServer):
    class Ping: ...

    async def handle_call(self, payload):
        match payload:
            case MockGenServer.Ping():
                return "pong"
        return ""

    @staticmethod
    async def ping():
        return await MockGenServer.call(MockGenServer.Ping())
