from __future__ import annotations

import json
from dataclasses import asdict, fields
from typing import Any, get_args, get_origin, get_type_hints

from src.homeworks.homework_4.task_1.json_parser import JsonReader
from src.homeworks.homework_4.task_1.ORMExceptions import FieldError, NotFoundFieldError, StrictError


class Descriptor:
    def __init__(
        self, field_name: str, field_type: type, reader: JsonReader, path: str, strict: bool = False, number: int = -1
    ) -> None:
        self.field_name = field_name
        self.field_type = field_type
        self.value = None
        self.reader = reader
        self.path = path
        self.strict = strict
        self.number = number

    def __set__(self, instance: object, value: Any) -> None:
        instance.__dict__[self.field_name] = value

    def __get__(self, instance: object, owner: Any) -> Any:
        if not isinstance(instance, ORM):
            raise FieldError("Filed must be an instance of APIMeta")
        value = instance.__dict__[self.field_name]
        if value:
            return value
        if self.number == -1:
            try:
                request_value = self.reader.read_from_obj(self.field_name, self.path)
            except NotFoundFieldError as e:
                if self.strict:
                    raise StrictError(e)
                request_value = None
        else:
            try:
                request_value = self.reader.read_from_list(f"{self.path}.{self.field_name}", self.number)
            except NotFoundFieldError as e:
                if self.strict:
                    raise StrictError(e)
                request_value = None
            self.number += 1
        if request_value is not None and not isinstance(request_value, self.field_type):
            raise TypeError(f"{self.field_name} must be {self.field_type}")
        return request_value

    def add_path(self) -> None:
        self.number = 0


class ORM:
    @classmethod
    def set_descriptors(cls: Any, reader: JsonReader, strict: bool = False, path: str = "", count: int = -1) -> Any:
        dataclass_fields = fields(cls)
        for field in dataclass_fields:
            field_type = field.type
            inner_type = get_args(field_type)[0] if get_args(field_type) else None
            origin_type = get_origin(field_type)
            if origin_type and issubclass(inner_type, ORM):
                length = reader.get_length_of_list(f"item")
                dataclasses = [
                    inner_type.set_descriptors(reader, strict, f"item", n_count) for n_count in range(length)
                ]
                setattr(
                    cls,
                    field.name,
                    dataclasses,
                )
            elif issubclass(get_type_hints(cls)[field.name], ORM):
                new_path = f"{path}.{field.name}" if path != "" else field.name
                setattr(cls, field.name, field_type.set_descriptors(reader, strict, new_path, count))
            else:
                if field.name in cls.__dict__ and count != -1:
                    cls.__dict__[field.name].add_path()
                else:
                    field_type = origin_type if origin_type else field_type
                    setattr(
                        cls,
                        field.name,
                        Descriptor(field.name, field_type, reader, path, strict, count),
                    )
        return cls

    @classmethod
    def set_dataclass(cls: Any, reader: JsonReader, strict: bool = False) -> Any:
        cls.set_descriptors(reader, strict)

        def set_recursion(cls: Any) -> ORM:
            args: list[ORM | list[ORM] | None] = []
            for field_name, filed_type in get_type_hints(cls).items():
                origin = get_origin(filed_type)
                sub = get_args(filed_type)[0] if origin else None
                if issubclass(filed_type, ORM):
                    args.append(set_recursion(filed_type))
                elif origin and issubclass(sub, ORM):
                    args.append([set_recursion(key) for key in cls.__dict__[field_name]])
                else:
                    args.append(None)
            return cls(*args)

        return set_recursion(cls)


class DataClassDumper:
    def dump(self, data_class: Any, name: str) -> None:
        dataclass_dict = asdict(data_class)
        json_str = json.dumps(dataclass_dict, indent=2)
        with open(f"{name}.json", "x") as f:
            f.write(json_str)
