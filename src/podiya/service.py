from typing import Dict, Protocol


class AggregateRepositoryProtocol(Protocol):
    async def get_by_id(id): ...


class Service:
    def __init__(self) -> None:
        self._aggregate_repository = None
        self._snapshot_repository = None
        self._event_store = None

        self._command_handlers: Dict = {}

    def command_handler(self, command_cls, handler):
        self._command_handlers[command_cls] = handler

    def execute_command(self, command):
        handler = self._command_handlers.get(command.__class__, None)
        if not handler:
            return False

        event = handler(command)
        self._event_store.persist(event)
