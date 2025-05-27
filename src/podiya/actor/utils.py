import asyncio
import inspect


def behavior_to_coro(behavior):
    iscorofun = inspect.iscoroutinefunction(behavior)
    isfun = inspect.isfunction(behavior)
    if iscorofun:
        return behavior()
    elif isfun:
        return asyncio.threads.to_thread(behavior)
    elif asyncio.iscoroutine(behavior):
        return behavior
    elif hasattr(behavior, '__call__'):
        return behavior_to_coro(getattr(behavior, '__call__'))
    else:
        raise ValueError("Bad behavior, should be callable or async callable")
