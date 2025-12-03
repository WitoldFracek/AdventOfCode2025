from abc import ABC
from typing import Callable
from utils.errors import panic

class Result[K, E](ABC):

    def __repr__(self) -> str:
        match self:
            case Ok(value): return f"Ok({value})"
            case Err(error): return f"Err({error})"

    def map[U](self, mapper: Callable[[K], U]) -> "Result[U, E]":
        match self:
            case Ok(value): return Ok(mapper(value))
            case Err(error): return Err(error)

    def and_[U](self, res: "Result[U, E]") -> "Result[U, E]":
        match self:
            case Ok(_): return res
            case Err(error): return Err(error)

    def and_then[U](self, mapper: Callable[[K], "Result[U, E]"]) -> "Result[U, E]":
        match self:
            case Ok(value): return mapper(value)
            case Err(error): return Err(error)

    def or_[F](self, res: "Result[K, F]") -> "Result[K, F]":
        match self:
            case Ok(value): return Ok(value)
            case Err(_): return res

    def or_else[F](self, mapper: Callable[[E], "Result[K, F]"]) -> "Result[K, F]":
        match self:
            case Ok(value): return Ok(value)
            case Err(error): return mapper(error)

    @property
    def is_ok(self) -> bool:
        match self:
            case Ok(_): return True
            case Err(_): return False

    @property
    def is_err(self) -> bool:
        return not self.is_ok

    def is_ok_and(self, predicate: Callable[[K], bool]) -> bool:
        match self:
            case Ok(value): return predicate(value)
            case Err(_): return False

    def is_err_and(self, predicate: Callable[[E], bool]) -> bool:
        match self:
            case Ok(_): return False
            case Err(error): return predicate(error)

    def ok(self) -> "Option[K]":
        from utils.option import Some, None_
        match self:
            case Ok(value): return Some(value)
            case Err(_): return None_()

    def err(self) -> "Option[E]":
        from utils.option import Some, None_
        match self:
            case Ok(_): return None_()
            case Err(error): return Some(error)

    def map_or[U](self, mapper: Callable[[K], U], default: U) -> U:
        match self:
            case Ok(value): return mapper(value)
            case Err(_): return default

    def map_or_else[U](self, mapper: Callable[[K], U], default_fn: Callable[[], U]) -> U:
        match self:
            case Ok(value): return mapper(value)
            case Err(_): return default_fn()

    def map_err[F](self, mapper: Callable[[E], F]) -> "Result[K, F]":
        match self:
            case Ok(value): return Ok(value)
            case Err(error): return Err(mapper(error))

    def inspect(self, action: Callable[[K], None]) -> "Result[K, E]":
        match self:
            case Ok(value):
                action(value)
                return self
            case Err(_):
                return self

    def inspect_err(self, action: Callable[[E], None]) -> "Result[K, E]":
        match self:
            case Ok(_):
                return self
            case Err(error):
                action(error)
                return self

    def expect(self, msg: str) -> K:
        match self:
            case Ok(value): return value
            case Err(_): raise panic(msg)

    def expect_err(self, msg: str) -> E:
        match self:
            case Ok(_): raise panic(msg)
            case Err(error): return error

    def unwrap(self) -> K:
        match self:
            case Ok(value): return value
            case Err(_): panic("Called unwrap on an Err value")

    def unwrap_or(self, default: K) -> K:
        match self:
            case Ok(value): return value
            case Err(_): return default

    def unwrap_or_else(self, default_fn: Callable[[], K]) -> K:
        match self:
            case Ok(value): return value
            case Err(_): return default_fn()

    def unwrap_err(self) -> E:
        match self:
            case Ok(_): panic("Called unwrap_err on an Ok value")
            case Err(error): return error


class Ok[T, E](Result[T, E]):
    __match_args__ = ('_value',)

    def __init__(self, value: T):
        self._value = value


class Err[T, E](Result[T, E]):
    __match_args__ = ('_error',)

    def __init__(self, error: E):
        self._error = error