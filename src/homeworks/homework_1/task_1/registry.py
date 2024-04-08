from typing import Callable, Generic, MutableMapping, Optional, Type, TypeVar

T = TypeVar("T")


class Registry(Generic[T]):
    def __init__(self, default: Optional[Type[T]] = None) -> None:
        self.default = default
        self.register_of_names: dict[str, Type[T]] = {}

    def register(self, name: str) -> Callable:
        def decorator(cls: Type[T]) -> Type[T]:
            if name in self.register_of_names:
                raise ValueError("This name is already registered")
            self.register_of_names[name] = cls
            return cls

        return decorator

    def dispatch(self, name: str) -> Type[T]:
        if name in self.register_of_names:
            return self.register_of_names[name]
        if self.default is None:
            raise ValueError(f"{name} realisation not registered")
        return self.default


if __name__ == "__main__":
    reg = Registry[MutableMapping]()

    @reg.register("AVL")
    class AVL(dict):
        pass

    @reg.register("Trep")
    class Trep(dict):
        pass

    @reg.register("HashTable")
    class HashTable(dict):
        pass

    print("In Registry collected 3 dict subclasses. You can choose any of them by name")
    print(f"name: AVL, class: {reg.dispatch('AVL')}")
    print(f"name: Trep, class: {reg.dispatch('Trep')}")
    print(f"name: HashTable, class: {reg.dispatch('HashTable')}")
