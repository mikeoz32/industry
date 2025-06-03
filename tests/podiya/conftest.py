import pytest
import pytest_asyncio

from podiya.actor.system import Kernel


@pytest_asyncio.fixture(scope="function")
async def kernel():
    async with Kernel("test_node"):
        yield
