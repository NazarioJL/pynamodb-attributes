from enum import Enum
from typing import Any
from typing import Generic
from typing import Optional
from typing import Type
from typing import TYPE_CHECKING
from typing import TypeVar

from pynamodb.attributes import Attribute

T = TypeVar('T', bound=Enum)
_fail: Any = object()


class EnumAttribute(Attribute, Generic[T]):

    attr_type = None

    def __init__(self, enum_type: Type[T], unknown_value: Optional[T] = _fail, **kwargs: Any) -> None:
        """
        :param enum_type: The type of the enum
        """
        super().__init__(**kwargs)
        self.enum_type = enum_type
        self.unknown_value = unknown_value
        if not all(isinstance(e.value, str) for e in self.enum_type):
            raise TypeError(f"Enumeration '{self.enum_type}' values must be all {self.attr_type}")

    def deserialize(self, value: str) -> Optional[T]:
        try:
            return self.enum_type(value)
        except ValueError:
            if self.unknown_value is _fail:
                raise
            return self.unknown_value

    def serialize(self, value: T) -> str:
        if not isinstance(value, self.enum_type):
            raise TypeError(f"value has invalid type '{type(value)}'; expected '{self.enum_type}'")
        return value.value

    if TYPE_CHECKING:
        def __get__(self, instance: Any, owner: Any) -> T:
            ...
