from typing import Any, Optional
from functools import singledispatchmethod

from industry.accounts.entity.user import User
from industry.accounts.events.user import UserDisabledEvent, UserRegisteredEvent


class UserMutator:
    def __call__(self, event: Any, state: Optional[Any]) -> Any:
        return self.on(event, state)

    @singledispatchmethod
    def on(cls, event: Any, state: Optional[Any]): ...

    @on.register
    def _(cls, event: UserRegisteredEvent, state: Optional[User]):
        return User(**event.model_dump())

    @on.register
    def _(cls, event: UserDisabledEvent, state: User):
        return state.model_copy(update=dict(disabled=True))
