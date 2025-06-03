import asyncio
import pytest

from podiya.actor.genserver import GenServer
from podiya.actor.supervisor import Supervisor
from tests.podiya.mocks import MockGenServer

pytestmark = pytest.mark.asyncio


async def test_supervisor_spawn_children(kernel):
    sup = Supervisor.start([MockGenServer()])
    await asyncio.sleep(0.1)

    res = await MockGenServer.ping()
    assert res
