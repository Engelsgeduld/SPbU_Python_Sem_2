from __future__ import annotations

import json
from dataclasses import asdict, fields
from typing import Any, get_args, get_origin, get_type_hints

from src.homeworks.homework_4.task_1.json_parser import JsonReader
from src.homeworks.homework_4.task_1.ORMExceptions import FieldError, NotFoundFieldError, StrictError


class Descriptor:
    def __init__(
        self, field_name: str, field_type: Any, reader: JsonReader, path: str, strict: bool = False, value: Any = None
    ) -> None:
        self.field_name = field_name
        self.field_type = field_type
        self.reader = reader
        self.path = path
        self.strict = strict
        self.value = value

    def __set__(self, instance: object, value: Any) -> None:
        instance.__dict__[self.field_name] = value

    def __get__(self, instance: object, owner: Any) -> Any:
        if not isinstance(instance, ORM):
            raise FieldError("Field must be an instance of APIMeta")
        value = instance.__dict__[self.field_name]
        if value:
            return value
        if isinstance(self.value, list):
            inited_dataclasses = [data_cls(*[None] * len(fields(data_cls))) for data_cls in self.value]
            instance.__dict__[self.field_name] = inited_dataclasses
            return inited_dataclasses
        if self.value:
            data_cls = self.field_type(*[None] * len(fields(self.field_type)))
            instance.__dict__[self.field_name] = data_cls
            return data_cls
        try:
            request_value = self.reader.get_data(self.path, self.field_name)
        except NotFoundFieldError as e:
            if self.strict:
                raise StrictError(e)
            request_value = None
        if request_value is not None and not isinstance(request_value, self.field_type):
            raise TypeError(f"{self.field_name} must be {self.field_type}")
        instance.__dict__[self.field_name] = request_value
        return request_value


class ORM:
    @classmethod
    def set_descriptors(cls: Any, reader: JsonReader, strict: bool = False, path: str = "") -> Any:
        dataclass_fields = fields(cls)
        for field in dataclass_fields:
            field_type = field.type
            inner_type = get_args(field_type)[0] if get_args(field_type) else None
            origin_type = get_origin(field_type)
            if origin_type and issubclass(inner_type, ORM):
                length = reader.get_length_of_list(f"item")
                dataclasses = [inner_type.set_descriptors(reader, strict, f"item") for _ in range(length)]
                setattr(
                    cls,
                    field.name,
                    Descriptor(field.name, field_type, reader, path, strict, dataclasses),
                )
            elif issubclass(get_type_hints(cls)[field.name], ORM):
                new_path = f"{path}.{field.name}" if path != "" else field.name
                descriptor_args = [
                    field.name,
                    field_type,
                    reader,
                    path,
                    strict,
                    field_type.set_descriptors(reader, strict, new_path),
                ]
                setattr(cls, field.name, Descriptor(*descriptor_args))
            else:
                field_type = origin_type if origin_type else field_type
                setattr(
                    cls,
                    field.name,
                    Descriptor(field.name, field_type, reader, path, strict),
                )
        return cls

    @classmethod
    def set_dataclass(cls: Any, reader: JsonReader, strict: bool = False) -> Any:
        cls.set_descriptors(reader, strict)
        args = [None] * len(fields(cls))
        return cls(*args)

    def dump(self: Any, name: str) -> None:
        dataclass_dict = asdict(self)
        json_str = json.dumps(dataclass_dict, indent=2)
        with open(f"{name}.json", "x") as f:
            f.write(json_str)
