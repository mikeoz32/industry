from datetime import datetime
from typing import Any
from industry.accounts.entity.user import UserId
from industry.accounts.events.user import UserRegisteredEvent
from industry.accounts.repository.user import UserRepositoryProtocol


class CreateUserCommand:
    def __init__(self, repository: UserRepositoryProtocol) -> None:
        self.repo = repository

    async def __call__(self, identity_id: str, email: str, nickname: str) -> Any:
        user_id = UserId.from_identity(identity_id)
        user = await self.repo.get(user_id)
        if user:
            raise Exception("User already exists")
        return UserRegisteredEvent(
            user_id=user_id, identity_id=identity_id, email=email, nickname=nickname, created_at=datetime.now()
        )
