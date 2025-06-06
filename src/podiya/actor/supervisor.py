from typing import List, Optional, Protocol

from podiya.actor.process import monitor, receive, spawn, start
from podiya.actor.process.pid import PID
from podiya.actor.process.process import Process


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
        return self._name


class Supervisor:
    def __init__(self, children: List[ChildSpecProtocol] = None) -> None:
        self._children = children or []
        self._active: dict[PID, ChildSpecProtocol] = dict()

    def init(self):
        """
        Concrete supervisers should add thair children
        ```
            class MySupervisor(Supervisor):
                def init(self):
                    self._children = [MyGenserver]
        ```
        """

    async def __call__(self) -> None:
        self.init()
        self.spawn_children()
        async for envelope in receive():
            match envelope.payload:
                case Process.Down(pid=pid, reason=_):
                    self.restart(pid)

    def restart(self, pid):
        child = self._active.get(pid, None)
        if child:
            del self._active[pid]
            pid = start(child.behavior, child.name)
            self._active[pid] = child
            monitor(pid)

    def spawn_children(self):
        for child in self._children:
            pid = start(child.behavior, child.name)
            self._active[pid] = child
            monitor(pid)

    @classmethod
    def start(cls, children: List[ChildSpecProtocol] = None):
        return start(cls(children), cls.__qualname__)
