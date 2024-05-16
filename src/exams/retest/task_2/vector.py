from abc import ABCMeta
from typing import Any, Generic, TypeVar


class ArithmeticAvailable(metaclass=ABCMeta):
    @classmethod
    def __subclasshook__(cls, instance: Any) -> bool:
        return (
            hasattr(instance, "__add__")
            and hasattr(instance, "__sub__")
            and hasattr(instance, "__mul__")
            and hasattr(instance, "__pow__")
        )

    def __add__(self, other: "ArithmeticAvailable") -> "ArithmeticAvailable":
        raise NotImplementedError

    def __sub__(self, other: "ArithmeticAvailable") -> "ArithmeticAvailable":
        raise NotImplementedError

    def __mul__(self, other: "ArithmeticAvailable") -> "ArithmeticAvailable":
        raise NotImplementedError


T = TypeVar("T", ArithmeticAvailable, float, bool, int)


class VectorLengthError(Exception):
    def __init__(self, message: str = "") -> None:
        super().__init__(message)


class EqualError(Exception):
    def __init__(self, message: str = "") -> None:
        super().__init__(message)


class Vector(Generic[T]):
    def __init__(self, coords: list[T]) -> None:
        if any(map(lambda x: not isinstance(x, ArithmeticAvailable), coords)):
            raise TypeError("All coordinates types must support add, sub and mul")
        self.coords: list[T] = coords

    def __len__(self) -> int:
        return len(self.coords)

    @staticmethod
    def _len_check(first_vector: "Vector", second_vector: "Vector") -> None:
        if len(first_vector) != len(second_vector):
            raise VectorLengthError("Vectors must be same dimension")

    def __add__(self, other: "Vector") -> "Vector":
        self._len_check(self, other)
        new_coords = list(map(lambda x, y: x + y, self.coords, other.coords))
        return Vector(new_coords)

    def __sub__(self, other: "Vector") -> "Vector":
        self._len_check(self, other)
        new_coords = list(map(lambda x, y: x - y, self.coords, other.coords))
        return Vector(new_coords)

    def is_zero(self) -> bool:
        return not any(self.coords)

    def __mul__(self, vector: "Vector") -> T | int:
        self._len_check(self, vector)
        return sum(list(map(lambda x, y: x * y, self.coords, vector.coords)))

    def __matmul__(self, vector: "Vector") -> "Vector":
        if len(self) != 3:
            raise VectorLengthError("Vector product support 3 dimensional vectors only")
        self._len_check(self, vector)
        first_coord = self.coords[1] * vector.coords[2] - self.coords[2] * vector.coords[1]
        second_coord = self.coords[2] * vector.coords[0] - self.coords[0] * vector.coords[2]
        third_coord = self.coords[0] * vector.coords[1] - self.coords[1] * vector.coords[0]
        return Vector([first_coord, second_coord, third_coord])

    def __str__(self) -> str:
        return f"Vector: ({self.coords})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Vector):
            raise EqualError(f"Cannot compare Vector and {type(other)}")
        self._len_check(self, other)
        return all(map(lambda pair: pair[0] == pair[1], zip(self.coords, other.coords)))
