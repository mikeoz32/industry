from typing import Generic, Optional, TypeVar

S = TypeVar("State")


class Aggregate(Generic[S]):
    def __init__(self, initial_state: Optional[S] = None) -> None:
        self._state = initial_state or None
