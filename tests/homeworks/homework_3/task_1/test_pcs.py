from copy import deepcopy
from inspect import getfullargspec
from random import choice, choices, randint

import hypothesis.strategies as st
import pytest
from hypothesis import given

from src.homeworks.homework_3.task_1.PerformedCommandStorage import *
from src.homeworks.homework_3.task_1.StorageExceptions import *


class TestActionsInvariant:
    def collection_generator(self, length: int):
        collection = [randint(-150, 150) for _ in range(length)]
        copy_collection = deepcopy(collection)
        return collection, copy_collection

    @given(st.integers(1, 1000))
    def test_front_insert(self, length: int):
        collection, copy_collection = self.collection_generator(length)
        item = randint(-150, 150)
        front_insert = FrontInsert(item)
        front_insert.forward(collection)
        assert collection == [item, *copy_collection]
        front_insert.backward(collection)
        assert collection == copy_collection

    @given(st.integers(1, 1000))
    def test_back_insert(self, length: int):
        collection, copy_collection = self.collection_generator(length)
        item = randint(-150, 150)
        back_insert = BackInsert(item)
        back_insert.forward(collection)
        assert collection == [*copy_collection, item]
        back_insert.backward(collection)
        assert collection == copy_collection

    @given(st.integers(1, 1000))
    def test_front_delete(self, length: int):
        collection, copy_collection = self.collection_generator(length)
        front_delete = FrontDelete()
        front_delete.forward(collection)
        assert collection == copy_collection[1:]
        front_delete.backward(collection)
        assert collection == copy_collection

    @given(st.integers(1, 1000))
    def test_back_delete(self, length: int):
        collection, copy_collection = self.collection_generator(length)
        back_delete = BackDelete()
        back_delete.forward(collection)
        assert collection == copy_collection[:-1]
        back_delete.backward(collection)
        assert collection == copy_collection

    @given(st.integers(1, 1000))
    def test_addition(self, length: int):
        collection, copy_collection = self.collection_generator(length)
        index = choice(range(length))
        value = randint(-100, 100)
        addition = Addition(index, value)
        addition.forward(collection)
        assert collection[index] == copy_collection[index] + value
        addition.backward(collection)
        assert collection == copy_collection

    @given(st.integers(2, 1000))
    def test_move(self, length: int):
        collection, copy_collection = self.collection_generator(length)
        indexes = choices(range(length), k=2)
        move = Move(*indexes)
        move.forward(collection)
        assert (collection[indexes[1]], collection[indexes[0]]) == (
            copy_collection[indexes[0]],
            copy_collection[indexes[1]],
        )
        move.backward(collection)
        assert collection == copy_collection

    @given(st.integers(1, 1000))
    def test_transit_element(self, length: int) -> None:
        collection, copy_collection = self.collection_generator(length)
        indexes = choices(range(length), k=2)
        transit = TransitElement(*indexes)
        transit.forward(collection)
        assert collection[indexes[1]] == copy_collection[indexes[0]]

    @given(st.integers(1, 1000))
    def test_transit_element(self, length: int) -> None:
        collection, copy_collection = self.collection_generator(length)
        sum_add = SumAdd()
        sum_add.forward(collection)
        assert collection == copy_collection + [sum(copy_collection)]


class TestActionUnit:
    @pytest.mark.parametrize(
        "collection, expected",
        [([1, 2, 3, 4], [-1, -2, -3, -4]), ([-1, 2, -3, 4], [1, -2, 3, -4]), ([1, 2, 3, 4], [-1, -2, -3, -4])],
    )
    def test_sign_change_action(self, collection, expected):
        copy_collection = deepcopy(collection)
        sign_change = SignChange()
        sign_change.forward(collection)
        assert collection == expected
        sign_change.backward(collection)
        assert collection == copy_collection


class TestActionExceptions:
    def test_move_range_exception(self):
        collection = [1, 2, 3, 4]
        move = Move(1, 5)
        with pytest.raises(IndexError):
            move.forward(collection)

    def test_move_neg_range_exception(self):
        collection = [1, 2, 3, 4]
        move = Move(-1, 5)
        with pytest.raises(IndexError):
            move.forward(collection)

    def test_move_length_exception(self):
        collection = [1]
        move = Move(0, 0)
        with pytest.raises(ValueError):
            move.forward(collection)

    def test_addition_exception(self):
        collection = [1, 2, 3, 4]
        addition = Addition(5, 0)
        with pytest.raises(IndexError):
            addition.forward(collection)

    def test_multiply_exception(self):
        collection = [1, 2, 3, 4]
        multiply = Multiply(5, 2)
        with pytest.raises(IndexError):
            multiply.forward(collection)

    def test_front_delete(self):
        collection = []
        front_delete = FrontDelete()
        with pytest.raises(ValueError):
            front_delete.forward(collection)

    def test_back_delete(self):
        collection = []
        back_delete = BackDelete()
        with pytest.raises(ValueError):
            back_delete.forward(collection)

    def test_sum_add_exception(self):
        collection = []
        sum_add = SumAdd()
        with pytest.raises(ValueError):
            sum_add.forward(collection)


class TestPCS:
    @given(st.integers(1, 50))
    def test_pcs_invariant(self, count):
        collection = [randint(-100, 100) for _ in range(500)]
        copy_collection = deepcopy(collection)
        pcs = PerformedCommandStorage(collection)
        register = ACTIONS_REGISTRY
        all_actions = register.register_of_names
        actions = [all_actions[name] for name in all_actions.keys()]
        for action in actions:
            args_count = len(getfullargspec(action.__init__).args[1:])
            args = [randint(0, 100) for _ in range(args_count)]
            imp_action = action(*args)
            pcs.apply(imp_action)
        for _ in range(len(actions)):
            pcs.redo()
        assert collection == copy_collection

    def test_pcs_empy_action_list_exception(self):
        collection = []
        pcs = PerformedCommandStorage(collection)
        with pytest.raises(EmptyActionListError):
            pcs.redo()

    def test_collection_exception(self):
        collection = {}
        with pytest.raises(NotSupportedCollectionTypeError):
            pcs = PerformedCommandStorage(collection)


class TestParsers:
    def test_insert_parser(self):
        parser = InsertArgsParse()
        with pytest.raises(ValueError):
            parser.args_validation(["123", "123"])
        with pytest.raises(ValueError):
            parser.args_validation(["abc"])

    def test_addition_parser(self):
        parser = MoveAdditionArgsParse()
        with pytest.raises(ValueError):
            parser.args_validation(["123"])
        with pytest.raises(ValueError):
            parser.args_validation(["abc", "123"])

    def test_no_args_parser(self):
        parser = NoArgsActionParse()
        with pytest.raises(ValueError):
            parser.args_validation(["1"])
