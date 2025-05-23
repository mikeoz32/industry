from datetime import datetime

from pydantic import BaseModel

from industry.accounts.entity.user import UserId


class UserRegisteredEvent(BaseModel, frozen=True):
    user_id: UserId
    identity_id: str

    email: str
    nickname: str
    created_at: datetime


class UserDisabledEvent(BaseModel, frozen=True):
    user_id: UserId
