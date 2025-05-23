from typing import Any, Optional
from uuid import UUID, NAMESPACE_URL, uuid5
from dataclasses import Field, asdict, dataclass, asdict
from datetime import datetime
from functools import singledispatchmethod

from industry.accounts.events.user import UserDisabledEvent, UserRegisteredEvent


class UserId:
    """
    User Id Value Object
    """

    id: UUID

    @staticmethod
    def from_identity(identity_id: str):
        return UserId(id=uuid5(NAMESPACE_URL, f"/users/{identity_id}"))


@dataclass(frozen=True)
class User:
    """
    User root entity
    """

    id: UserId
    identity_id: str

    # duplicate some data from identity provider
    email: str
    nickname: str
    created_at: datetime
    disabled: bool = Field(default=True)


class UserMutator:
    def __call__(self, event: Any, state: Optional[Any]) -> Any:
        return self.on(event, state)

    @singledispatchmethod
    def on(event: Any, state: Optional[Any]): ...

    @on.register()
    def _(event: UserRegisteredEvent, state: Optional[User]):
        return User(**asdict(event))

    @on.register()
    def _(event: UserDisabledEvent, state: User):
        new_state = asdict(state)
        new_state.update(disabled=True)
        return User(**new_state)
