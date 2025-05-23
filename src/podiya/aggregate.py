from typing import Any, Callable, Generic, List, Optional, TypeVar

S = TypeVar("State")

Mutator = Callable[[Any, Optional[S]], S]


class Aggregate(Generic[S]):
    def __init__(self, initial_state: Optional[S] = None) -> None:
        self._state = initial_state or None
        self._mutator: Mutator = lambda _, s: s
        self._version = 0

    def apply(self, event: Any):
        self._state = self._mutator(event, self._state)
