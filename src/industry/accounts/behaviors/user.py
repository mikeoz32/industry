from datetime import datetime
from typing import Optional
from industry.accounts.entity.user import User, UserId
from industry.accounts.events.user import UserDisabledEvent, UserRegisteredEvent


class UserBehavior:
    @staticmethod
    def register(
        state: Optional[User],
        identity_id: str,
        email: str,
        nickname: str,
        created_at: datetime,
    ):
        if state:
            raise Exception("Invalid state")
        return UserRegisteredEvent(
            user_id=UserId.from_identity(identity_id),
            identity_id=identity_id,
            email=email,
            nickname=nickname,
            created_at=created_at,
        )

    @staticmethod
    def disable(state: User):
        if state.disabled:
            raise Exception("Invalid state")
        return UserDisabledEvent(user_id=state.user_id)
