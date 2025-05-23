from typing import Any, Callable, Generic, List, Optional, TypeVar

S = TypeVar("State")

Mutator = Callable[[Any, Optional[S]], S]


def default_mutator(_, s):
    return s


class Aggregate(Generic[S]):
    def __init__(
        self,
        initial_state: Optional[S] = None,
        behavior: Optional[Any] = None,
        mutator: Optional[Mutator] = None,
    ) -> None:
        self._state = initial_state or None
        self._mutator = mutator or default_mutator
        self._behavior = behavior
        self._version = 0

    def apply(self, event: Any):
        self._state = self._mutator(event, self._state)
        self._version += 1

    def __getattr__(self, name: str):
        if self._behavior and hasattr(self._behavior, name):
            attr = getattr(self._behavior, name)

            # Якщо це метод — обгортаємо його так, щоб він мав доступ до self.state
            if callable(attr):

                def wrapped(*args, **kwargs):
                    result = attr(self._state, *args, **kwargs)

                    # Події можуть бути або одиничною подією, або списком
                    events = [result] if not isinstance(result, list) else result
                    for event in events:
                        self.apply(event)
                    return result

                return wrapped

            return attr

        raise AttributeError(
            f"'{type(self).__name__}' object has no attribute '{name}'"
        )
