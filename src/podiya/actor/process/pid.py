
from uuid import uuid4


class PID:
    def __init__(self) -> None:
        self._id = uuid4()
        self._address = "local"

    @property
    def address(self):
        return self._address

    @property
    def id(self):
        return self._id

    def __repr__(self) -> str:
        return f"PID<{self._id}@{self._address}>"
