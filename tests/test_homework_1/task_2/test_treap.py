import random

import pytest

from src.homeworks.homework_1.task_2.treap import Treap


class TestTreapNormalScenario:
    TEST_TREE = Treap()

    @pytest.mark.parametrize("item, expected_len", [((1, 2), 1), ((2, "eee"), 2), ((0, 5), 3), ((111, 12), 4)])
    def test_setitem_normal_scenario(self, item, expected_len):
        self.TEST_TREE[item[0]] = item[1]
        assert item[0] in self.TEST_TREE and self.TEST_TREE.length == expected_len

    def test_iter_(self):
        assert [key for key in self.TEST_TREE] == [0, 1, 2, 111]

    @pytest.mark.parametrize("item", [(1, 2), (2, "eee"), (0, 5), (111, 12)])
    def test_get_element_normal_scenario(self, item):
        assert self.TEST_TREE[item[0]] == item[1]

    @pytest.mark.parametrize("key", [1, 2, 0])
    def test_pop_normal_scenario(self, key):
        expected_length = self.TEST_TREE.length - 1
        self.TEST_TREE.pop(key)
        assert key not in self.TEST_TREE and self.TEST_TREE.length == expected_length

    def test_pop_default_scenario(self):
        assert self.TEST_TREE.pop(222) is None

    def test_get_default_scenario(self):
        assert self.TEST_TREE.get(222) is None


class TestTreapExceptions:
    @pytest.fixture(scope="session", autouse=True)
    def test_tree(self):
        data = [(1, 2), (2, "eee"), (0, 5), (111, 12)]
        test_tree = Treap()
        for item in data:
            test_tree[item[0]] = item[1]
        return test_tree

    @staticmethod
    def create_empty_tree():
        return Treap()

    @pytest.mark.parametrize("item", [("111", 10), (1, 2), (None, 3)])
    def test_setitem_exception(self, item, test_tree):
        with pytest.raises(KeyError):
            test_tree[item[0]] = item[1]

    @pytest.mark.parametrize("key", [222, None, "333"])
    def test_get_element_exception(self, key, test_tree):
        with pytest.raises(KeyError):
            element = test_tree[key]

    def test_del_exception_wrong_key(self, test_tree):
        with pytest.raises(KeyError):
            del test_tree[222]

    def test_del_exception_empty_tree(self):
        empty_tree = self.create_empty_tree()
        with pytest.raises(IndexError):
            del empty_tree[1]


class TestTreapWithRandomValues:
    TEST_KEYS = [random.uniform(0, 10) for _ in range(1000)]
    TEST_VALUES = [random.uniform(0, 10) for _ in range(1000)]
    TEST_ITEMS = list(zip(TEST_KEYS, TEST_VALUES))
    RANDOM_TREE = Treap()

    @pytest.mark.parametrize("item", TEST_ITEMS)
    def test_setitem_with_random_values(self, item):
        self.RANDOM_TREE[item[0]] = item[1]
        assert item[0] in self.RANDOM_TREE

    @pytest.mark.parametrize("item", TEST_ITEMS)
    def test_get_with_random_values(self, item):
        assert self.RANDOM_TREE[item[0]] == item[1]

    @pytest.mark.parametrize("key", TEST_KEYS)
    def test_pop_with_random_values(self, key):
        self.RANDOM_TREE.pop(key)
        assert key not in self.RANDOM_TREE
