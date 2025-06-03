from enum import Enum, auto
from typing import Any, Optional, Tuple
from time import time_ns
from uuid import UUID, uuid4
from podiya.actor.process.pid import PID


class MessageType(Enum):
    USER = auto()
    SYSTEM = auto()


class Envelope:
    def __init__(
        self,
        sender: PID,
        payload: Any,
        timestamp: int = time_ns(),
        message_type: MessageType = MessageType.USER,
        correlation_id: Optional[UUID] = None,
    ) -> None:
        self._sender = sender
        self._payload = payload
        self._timestamp = timestamp
        self._id = uuid4()
        self._correlation_id = correlation_id or uuid4()
        self._message_type = message_type

    @property
    def sender(self):
        return self._sender

    @property
    def payload(self):
        return self._payload

    @property
    def id(self):
        return self._id

    @property
    def timestamp(self):
        return self._timestamp

    @property
    def correlation_id(self):
        return self._correlation_id

    @property
    def message_type(self) -> MessageType:
        return self._message_type
