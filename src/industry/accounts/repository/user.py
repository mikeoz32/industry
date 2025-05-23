from typing import Optional, Protocol

from industry.accounts.entity.user import User, UserId


class UserRepositoryProtocol(Protocol):
    async def get(id: UserId) -> Optional[User]: ...
