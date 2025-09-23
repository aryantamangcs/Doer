from contextvars import ContextVar

current_user: ContextVar = ContextVar("current_user")
