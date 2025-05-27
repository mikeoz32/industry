from podiya.actor.process import context
from podiya.actor.process.pid import PID
from podiya.actor.process.process import Process


class ProcessRegistry:
    def __init__(self) -> None:
        self._local_processes = dict()
        self._named_processes = dict()

    def register(self, pid: PID, process: Process):
        if pid.address == "local":
            self._local_processes[pid.id] = process

    def get(self, pid: PID) -> Process:
        return self._local_processes.get(pid.id)

    def register_named(self, name, pid):
        self._named_processes[name] = pid

    def get_named(self, name: str) -> Process:
        return self._named_processes.get(name, None)


def get_process_regisrty() -> ProcessRegistry:
    return context._process_regisrty.get()


def find_proc(pid: PID) -> Process | None:
    return get_process_regisrty().get(pid)
