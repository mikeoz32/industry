from typing import List, Optional
from uuid import UUID, NAMESPACE_URL, uuid5
from datetime import datetime
from pydantic import BaseModel, Field


class UserId(BaseModel, frozen=True):
    """
    User Id Value Object
    """

    id: UUID

    @staticmethod
    def from_identity(identity_id: str):
        return UserId(id=uuid5(NAMESPACE_URL, f"/users/{identity_id}"))


class UserFullName(BaseModel, frozen=True):
    first_name: str
    last_name: str


class UserEducationEntry(BaseModel, frozen=True):
    end_year: int
    speciality: str
    degree: str


class User(BaseModel, frozen=True):
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

    # User profile data
    full_name: Optional[UserFullName] = None
    bio: str = ""
    education: List[UserEducationEntry] = Field(default_factory=list)
