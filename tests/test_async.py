import asyncio

import kolo
import pytest


async def async_add(*args: int) -> int:
    return sum(args)


async def slow_add(*args: int, time: float) -> int:
    await asyncio.sleep(time)
    return await async_add(*args)


async def multi_add():
    return await asyncio.gather(slow_add(1, 2, time=0.2), slow_add(3, 4, time=0.1))


@pytest.mark.parametrize("use_rust", (False, True))
def test_profile_tasks(use_rust):
    with kolo.enabled({"use_rust": use_rust}):
        results = asyncio.run(multi_add())
    assert results == [3, 7]
