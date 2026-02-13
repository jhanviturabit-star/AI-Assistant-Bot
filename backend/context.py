from contextvars import ContextVar

current_token = ContextVar("current_token", default=None)
