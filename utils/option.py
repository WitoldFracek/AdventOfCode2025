from abc import ABC
from typing import Callable, Tuple
from utils.errors import panic


class Option[T](ABC):

    @property
    def is_some(self) -> bool:
        match self:
            case Some(_): return True
            case None_(): return False

    @property
    def is_none(self) -> bool:
        return not self.is_some

    def is_some_and(self, predicate: Callable[[T], bool]) -> bool:
        match self:
            case Some(value): return predicate(value)
            case None_(): return False

    def is_none_or(self, predicate: Callable[[T], bool]) -> bool:
        match self:
            case Some(value): return predicate(value)
            case None_(): return True

    def map[U](self, mapper: Callable[[T], U]) -> "Option[U]":
        match self:
            case Some(value): return Some(mapper(value))
            case None_(): return None_()

    def map_or[U](self, mapper: Callable[[T], U], default: U) -> U:
        match self:
            case Some(value): return mapper(value)
            case None_(): return default

    def map_or_else[U](self, mapper: Callable[[T], U], default_fn: Callable[[], U]) -> U:
        match self:
            case Some(value): return mapper(value)
            case None_(): return default_fn()

    def flatmap[U](self, mapper: Callable[[T], "Option[U]"]) -> "Option[U]":
        match self:
            case Some(value): return mapper(value)
            case None_(): return None_()

    def expect(self, msg: str) -> T:
        match self:
            case Some(value): return value
            case None_(): panic(msg)

    def unwrap(self) -> T:
        match self:
            case Some(value): return value
            case None_(): panic("called `Option.unwrap()` on a `None` value")

    def unwrap_or(self, default: T) -> T:
        match self:
            case Some(value): return value
            case None_(): return default

    def unwrap_or_else(self, default_fn: Callable[[], T]) -> T:
        match self:
            case Some(value): return value
            case None_(): return default_fn()

    def inspect(self, action: Callable[[T], None]) -> "Option[T]":
        match self:
            case Some(value):
                action(value)
                return self
            case None_(): return self

    def ok_or[E](self, err: E) -> "Result[T, E]":
        from utils.result import Err, Ok
        match self:
            case Some(value): return Ok(value)
            case None_(): return Err(err)

    def ok_or_else[E](self, err_fn: Callable[[], E]) -> "Result[T, E]":
        from utils.result import Err, Ok
        match self:
            case Some(value): return Ok(value)
            case None_(): return Err(err_fn())

    def and_(self, optb: "Option[T]") -> "Option[T]":
        match self:
            case Some(_): return optb
            case None_(): return None_()

    def and_then[U](self, f: Callable[[T], "Option[U]"]) -> "Option[U]":
        match self:
            case Some(value): return f(value)
            case None_(): return None_()

    def filter(self, predicate: Callable[[T], bool]) -> "Option[T]":
        match self:
            case Some(value) if predicate(value): return self
            case _: return None_()

    def or_(self, optb: "Option[T]") -> "Option[T]":
        match self:
            case Some(_): return self
            case None_(): return optb

    def or_else(self, f: Callable[[], "Option[T]"]) -> "Option[T]":
        match self:
            case Some(_): return self
            case None_(): return f()

    def xor(self, optb: "Option[T]") -> "Option[T]":
        match (self, optb):
            case (Some(_), None_()): return self
            case (None_(), Some(_)): return optb
            case _: return None_()

    def replace(self, new_value: T) -> "Option[T]":
        match self:
            case Some(old_value):
                self._value = new_value
                return Some(old_value)
            case None_(): return None_()

    def zip[U](self, other: "Option[U]") -> "Option[Tuple[T, U]]":
        match (self, other):
            case (Some(value1), Some(value2)): return Some((value1, value2))
            case _: return None_()

    def zip_with[U, V](self, f: Callable[[T, U], V], other: "Option[U]") -> "Option[V]":
        match (self, other):
            case (Some(value1), Some(value2)): return Some(f(value1, value2))
            case _: return None_()

    def __repr__(self) -> str:
        match self:
            case Some(value): return f"Some({value})"
            case None_(): return "None_()"



class Some[T](Option[T]):
    __match_args__ = ('value',)

    def __init__(self, value: T):
        self._value = value

    def __eq__(self, value):
        return isinstance(value, Some) and self._value == value._value


class None_[T](Option[T]):
    __match_args__ = ()

    def __eq__(self, value):
        return isinstance(value, None_)