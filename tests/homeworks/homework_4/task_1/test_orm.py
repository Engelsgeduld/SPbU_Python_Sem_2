import json
import os
import tempfile
from dataclasses import asdict, dataclass

import pytest
from faker import Faker

from src.homeworks.homework_4.task_1.json_orm import ORM, Descriptor
from src.homeworks.homework_4.task_1.json_parser import JsonReader
from src.homeworks.homework_4.task_1.ORMExceptions import *

fake = Faker()


@dataclass
class SomeNotORMClass:
    name: int


@dataclass
class Person(ORM):
    firstname: str
    lastname: str


@dataclass
class OtherPerson(ORM):
    firstname: str
    lastname: str
    notname: str


@dataclass
class Deep(ORM):
    person: Person


@dataclass
class MultiplyClassDeep(ORM):
    deep: Deep


@dataclass
class ListPersons(ORM):
    persons: list[OtherPerson]


@dataclass
class Bank(ORM):
    id: int
    balance: int


class TestORMNormal:
    def test_basic_scenario(self):
        fake = Faker()
        data = (fake.name(), fake.name())
        dataset = {"firstname": data[0], "lastname": data[1]}
        json_str = json.dumps(dataset, indent=2)
        with tempfile.NamedTemporaryFile(mode="w+", suffix=".json", delete=False) as json_file:
            json_file.write(json_str)
        name = json_file.name.replace(".json", "")
        reader = JsonReader(name)
        person = Person.set_dataclass(reader)
        assert person.firstname == data[0] and person.lastname == data[1]
        os.remove(json_file.name)

    def test_multiply_scenario(self):
        fake = Faker()
        data = (fake.name(), fake.name())
        dataset = {"deep": {"person": {"firstname": data[0], "lastname": data[1]}}}
        json_str = json.dumps(dataset, indent=2)
        with tempfile.NamedTemporaryFile(mode="w+", suffix=".json", delete=False) as json_file:
            json_file.write(json_str)
        name = json_file.name.replace(".json", "")
        reader = JsonReader(name)
        multiply = MultiplyClassDeep.set_dataclass(reader)
        assert multiply.deep.person.firstname == data[0] and multiply.deep.person.lastname == data[1]
        os.remove(json_file.name)

    def test_list_scenarios(self):
        fake = Faker()
        list_data = [(fake.name(), fake.name(), fake.name()) for _ in range(100)]
        dataset = [{"firstname": data[0], "lastname": data[1], "notname": data[2]} for data in list_data]
        json_str = json.dumps(dataset, indent=2)
        with tempfile.NamedTemporaryFile(mode="w+", suffix=".json", delete=False) as json_file:
            json_file.write(json_str)
        name = json_file.name.replace(".json", "")
        reader = JsonReader(name)
        list_persons = ListPersons.set_dataclass(reader)
        assert asdict(list_persons)["persons"] == dataset
        os.remove(json_file.name)


class TestORMExceptions:
    def test_field_type_exception(self):
        data = (fake.name(), fake.name())
        dataset = {"id": data[0], "balance": data[1]}
        json_str = json.dumps(dataset, indent=2)
        with tempfile.NamedTemporaryFile(mode="w+", suffix=".json", delete=False) as json_file:
            json_file.write(json_str)
        name = json_file.name.replace(".json", "")
        reader = JsonReader(name)
        bank = Bank.set_dataclass(reader)
        with pytest.raises(TypeError):
            balance = bank.balance

    def test_strict_mode_exception(self):
        dataset = {"id": 50}
        json_str = json.dumps(dataset, indent=2)
        with tempfile.NamedTemporaryFile(mode="w+", suffix=".json", delete=False) as json_file:
            json_file.write(json_str)
        name = json_file.name.replace(".json", "")
        reader = JsonReader(name)
        bank = Bank.set_dataclass(reader, True)
        with pytest.raises(StrictError):
            balance = bank.balance

    def test_field_exception(self):
        descriptor = Descriptor("name", int, JsonReader("empty"), "")
        setattr(SomeNotORMClass, "name", descriptor)
        with pytest.raises(FieldError):
            some_orm = SomeNotORMClass(5)
            name = some_orm.name
