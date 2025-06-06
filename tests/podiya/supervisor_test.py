import asyncio
import pytest

from podiya.actor.genserver import GenServer
from podiya.actor.supervisor import Supervisor
from tests.podiya.mocks import MockGenServer, MockSupervisor

pytestmark = pytest.mark.asyncio


async def test_supervisor_spawn_children(kernel):
    sup = Supervisor.start([MockGenServer()])
    await asyncio.sleep(0.1)

    res = await MockGenServer.ping()
    assert res


async def test_supervisor_init(kernel):
    MockSupervisor.start()
    await asyncio.sleep(0.1)

    res = await MockGenServer.ping()
    assert res


async def test_supervisor_child_error(kernel):
    MockSupervisor.start()
    await asyncio.sleep(0.1)

    await MockGenServer.trow("hi")
    print("Should handle restart")
    # await asyncio.sleep(1)
    print("Restart should be handled")

    try:
        res = await MockGenServer.ping()
    except BaseException as e:
        print(e)
    assert res
