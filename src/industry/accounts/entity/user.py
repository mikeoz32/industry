from uuid import UUID, NAMESPACE_URL, uuid5
from dataclasses import dataclass
from datetime import datetime


@dataclass()
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

    user_id: UserId
    identity_id: str

    # duplicate some data from identity provider
    email: str
    nickname: str
    created_at: datetime
    disabled: bool = False
