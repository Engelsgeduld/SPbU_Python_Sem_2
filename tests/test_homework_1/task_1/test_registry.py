from typing import Mapping

from src.homeworks.homework_1.task_1.registry import Registry
import pytest


MAPPING_REGISTER_1 = Registry(default=dict)[Mapping]
OBJECT_REGISTER_1 = Registry()[object]


@MAPPING_REGISTER_1.register(name="mapping")
class TestClassMapping(Mapping):
    def __init__(self):
        pass

    def __getitem__(self, key):
        pass

    def __iter__(self):
        pass

    def __len__(self):
        pass


class TestMappingSubclass(TestClassMapping):
    pass


@OBJECT_REGISTER_1.register(name="object")
class TestClassObj(object):
    pass


def test_registry_default():
    assert isinstance(MAPPING_REGISTER_1.dispatch("obj")(), dict)


def test_registry_dispatch():
    assert isinstance(MAPPING_REGISTER_1.dispatch("mapping")(), TestClassMapping)


def test_registry_wrong_parent_class():
    with pytest.raises(Exception):
        MAPPING_REGISTER_1.register(name="wrong")(TestClassObj)


def test_registry_dispatch_exception():
    with pytest.raises(Exception):
        OBJECT_REGISTER_1.dispatch("wrong")


def test_diff_registers():
    mapping_register_two = Registry()[Mapping]
    mapping_register_two.register(name = "dict")(dict)
    assert getattr(mapping_register_two, "register_of_names") != getattr(MAPPING_REGISTER_1, "register_of_names")


@pytest.mark.parametrize("name, cls", [("dict", dict), ("testmappingsubclass", TestMappingSubclass)])
def test_registry_normal(name, cls):
    MAPPING_REGISTER_1.register(name)(cls)
    assert isinstance(MAPPING_REGISTER_1.dispatch(name)(), cls)


