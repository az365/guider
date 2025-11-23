from typing import Union, Type, Callable

Numeric = Union[int, float]
NUMERIC = int, float

Primitives = Union[bool, int, float, str]
PRIMITIVES = bool, int, float, str

Array = Union[list, tuple]
ARRAY_TYPES = list, tuple
Collection = Union[Array, set]
COLLECTION_TYPES = *ARRAY_TYPES, set

Class = Union[Type, Callable]
