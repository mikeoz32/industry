from dataclasses import dataclass
from datetime import datetime

from industry.accounts.entity.user import UserId


@dataclass(frozen=True)
class UserRegisteredEvent:
    user_id: UserId
    identity_id: str

    email: str
    nickname: str
    created_at: datetime


@dataclass(frozen=True)
class UserDisabledEvent:
    user_id: UserId
