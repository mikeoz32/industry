from typing import List, Optional, Protocol

from podiya.actor.process import monitor, receive, spawn, start


class ChildSpecProtocol(Protocol):
    @property
    def behavior(self): ...

    @property
    def name(self): ...


class ChildSpec(ChildSpecProtocol):
    def __init__(
        self,
        behavior: Optional = None,
        *,
        name: Optional[str] = None,
    ) -> None:
        self._name = name
        self._behavior = behavior

    @property
    def behavior(self):
        return self._behavior

    def name(self):
        return self._behavior


class Supervisor:
    def __init__(self, children: List[ChildSpecProtocol]) -> None:
        self._children = children

    async def __call__(self) -> None:
        self.spawn_children()
        async for envelope in receive():
            ...

    def spawn_children(self):
        for child in self._children:
            pid = start(child.behavior, child.name)
            monitor(pid)

    @classmethod
    def start(cls, children: List[ChildSpecProtocol]):
        return start(cls(children), cls.__qualname__)
