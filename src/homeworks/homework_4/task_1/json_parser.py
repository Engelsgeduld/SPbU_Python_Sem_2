from typing import Any, Optional

import ijson

from src.homeworks.homework_4.task_1.ORMExceptions import NotFoundFieldError


class JsonReader:
    def __init__(self, file_name: str) -> None:
        self.file_name = file_name
        self.tracker: dict[str, int] = {}

    def read_from_obj(self, name: str, prefix: str) -> Optional[Any]:
        with open(f"{self.file_name}.json") as json_file:
            objects = ijson.kvitems(json_file, prefix)
            for key, value in objects:
                if key == name:
                    return value
            raise NotFoundFieldError(f"Field not found: {name}")

    def read_from_list(self, path: str, field_name: str, number: int) -> Optional[Any]:
        desc_prefix = f"{path}.{field_name}"
        with open(f"{self.file_name}.json") as json_file:
            objects = ijson.parse(json_file)
            count = 0
            for prefix, event, value in objects:
                if prefix == desc_prefix:
                    if count == number:
                        return value
                    count += 1
            raise NotFoundFieldError(f"Field not found: {desc_prefix}")

    def get_length_of_list(self, desc_prefix: str) -> int:
        with open(f"{self.file_name}.json") as json_file:
            objects = ijson.parse(json_file)
            count = 0
            for prefix, event, value in objects:
                if desc_prefix == prefix and event == "start_map":
                    count += 1
            return count

    def get_data(self, path: str, field_name: str) -> Optional[Any]:
        full_path = path + field_name
        if full_path not in self.tracker:
            self.tracker[full_path] = 0
        else:
            self.tracker[full_path] += 1
        if self.tracker[full_path] == 0:
            result = self.read_from_obj(field_name, path)
        else:
            result = self.read_from_list(path, field_name, self.tracker[full_path])
        return result