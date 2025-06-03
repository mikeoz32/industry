import asyncio
import pytest

from tests.podiya.mocks import MockGenServer

pytestmark = pytest.mark.asyncio


async def test_genserver_call(kernel):
    MockGenServer.start()
    await asyncio.sleep(0.1)
    res = await MockGenServer.ping()
    assert res == "pong"


async def test_genserver_child_spec():
    gs = MockGenServer()
    assert gs.behavior == gs
    assert gs.name == MockGenServer.__qualname__
