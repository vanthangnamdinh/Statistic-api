from contextlib import asynccontextmanager
from contextvars import ContextVar, Token
from enum import Enum
from typing import AsyncGenerator

from sqlalchemy.orm import DeclarativeBase

session_context: ContextVar[str] = ContextVar("session_context")


def get_session_context() -> str:
    return session_context.get()


def set_session_context(session_id: str) -> Token:
    return session_context.set(session_id)


def reset_session_context(context: Token) -> None:
    session_context.reset(context)



class Base(DeclarativeBase):
    ...