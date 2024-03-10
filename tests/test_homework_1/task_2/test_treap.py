import random

import pytest

from src.homeworks.homework_1.task_2.treap import Treap

TEST_KEYS = [random.uniform(0, 10) for _ in range(1000)]
TEST_VALUES = [random.uniform(0, 10) for _ in range(1000)]
TEST_ITEMS = list(zip(TEST_KEYS, TEST_VALUES))

TEST_TREE = Treap(int)
RANDOM_TREE = Treap(float)


def create_empty_tree():
    return Treap(int)


@pytest.mark.parametrize("item, expected_len", [((1, 2), 1), ((2, "eee"), 2), ((0, 5), 3), ((111, 12), 4)])
def test_setitem_normal_scenario(item, expected_len):
    TEST_TREE[item[0]] = item[1]
    assert item[0] in TEST_TREE and TEST_TREE.length == expected_len


def test_iter_():
    assert [key for key in TEST_TREE] == [0, 1, 2, 111]


@pytest.mark.parametrize("item", [("111", 10), (1, 2), (None, 3)])
def test_setitem_exception(item):
    with pytest.raises(KeyError):
        TEST_TREE[item[0]] = item[1]


@pytest.mark.parametrize("item", [(1, 2), (2, "eee"), (0, 5), (111, 12)])
def test_get_element_normal_scenario(item):
    assert TEST_TREE[item[0]] == item[1]


@pytest.mark.parametrize("key", [222, None, "333"])
def test_get_element_exception(key):
    with pytest.raises(KeyError):
        element = TEST_TREE[key]


@pytest.mark.parametrize("key", [1, 2, 0])
def test_pop_normal_scenario(key):
    expected_length = TEST_TREE.length - 1
    TEST_TREE.pop(key)
    assert key not in TEST_TREE and TEST_TREE.length == expected_length


def test_pop_default_scenario():
    assert TEST_TREE.pop(222) is None


def test_get_default_scenario():
    assert TEST_TREE.get(222) is None


def test_del_exception_wrong_key():
    with pytest.raises(KeyError):
        del TEST_TREE[222]


def test_del_exception_empty_tree():
    empty_tree = create_empty_tree()
    with pytest.raises(IndexError):
        del empty_tree[1]


@pytest.mark.parametrize("item", TEST_ITEMS)
def test_setitem_with_random_values(item):
    RANDOM_TREE[item[0]] = item[1]
    assert item[0] in RANDOM_TREE


@pytest.mark.parametrize("item", TEST_ITEMS)
def test_get_with_random_values(item):
    assert RANDOM_TREE[item[0]] == item[1]


@pytest.mark.parametrize("key", TEST_KEYS)
def test_pop_with_random_values(key):
    RANDOM_TREE.pop(key)
    assert key not in RANDOM_TREE
