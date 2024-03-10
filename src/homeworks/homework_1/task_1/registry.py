from typing import Callable, Self


class Registry:
    def __getitem__(self, item: type) -> Self:
        self.main_class = item
        return self

    def __init__(self, default: type = None) -> None:
        self.default = default
        self.register_of_names: dict[str, type] = {}

    def register(self, name: str) -> Callable:
        def decorator(cls: type) -> type:
            if not issubclass(cls, self.main_class):
                raise Exception(f"{cls.__name__} is not a subclass of {self.main_class.__name__}")
            self.register_of_names[name] = cls
            return cls

        return decorator

    def dispatch(self, name: str) -> type:
        if name in self.register_of_names:
            return self.register_of_names[name]
        if self.default is None:
            raise Exception(f"{name} realisation not registered")
        return self.default
