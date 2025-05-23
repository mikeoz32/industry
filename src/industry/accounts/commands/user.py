from datetime import datetime
from typing import Any

from pydantic import BaseModel
from industry.accounts.entity.user import UserId
from industry.accounts.events.user import UserRegisteredEvent
from industry.accounts.repository.user import UserRepositoryProtocol


class RegisterUserCommand(BaseModel, frozen=True):
    identity_id: str
    email: str
    nickname: str


class RegisterUserCommandHandler:
    def __init__(self, repository: UserRepositoryProtocol) -> None:
        self.repo = repository

    async def __call__(self, command: RegisterUserCommand) -> Any:
        user_id = UserId.from_identity(command.identity_id)
        user = await self.repo.get(user_id)
        if user:
            raise Exception("User already exists")
        return UserRegisteredEvent(
            user_id=user_id,
            identity_id=command.identity_id,
            email=command.email,
            nickname=command.nickname,
            created_at=datetime.now(),
        )
