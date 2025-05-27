import contextvars


_current_pid = contextvars.ContextVar("_current_pid")
_current_receive = contextvars.ContextVar("_current_receive")


_process_regisrty = contextvars.ContextVar("process_registry")
