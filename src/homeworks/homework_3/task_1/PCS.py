from typing import MutableSequence, Type

from src.homeworks.homework_1.task_1.registry import Registry


class Action:
    def standard_func(self, collection: MutableSequence[int]) -> None:
        pass

    def redo_func(self, collection: MutableSequence[int]) -> None:
        pass

    def validation(self, collection: MutableSequence[int]) -> None:
        pass

    @staticmethod
    def args_validation(args: list[str]) -> list:
        return []


class EmptyActionListError(Exception):
    def __init__(self) -> None:
        super().__init__("Actions list is empty. Nothing to redo")


class NoImplementedActionError(Exception):
    def __init__(self, action_name: str) -> None:
        super().__init__(f"{action_name} is not implemented")


class NotSupportedCollectionTypeError(Exception):
    def __init__(self, collection_type: str) -> None:
        super().__init__(f"{collection_type} is not supported")


ACTIONS_REGISTRY = Registry[Action]()


class ActionRegistry:
    def __init__(self) -> None:
        self.registry = ACTIONS_REGISTRY

    def __getitem__(self, name: str) -> Type[Action]:
        try:
            return self.registry.dispatch(name)
        except ValueError:
            raise NoImplementedActionError(name)

    def all_actions(self) -> dict[str, Type[Action]]:
        return self.registry.register_of_names


class NoArgsActionParse:
    @staticmethod
    def args_validation(args: list[str]) -> list:
        if len(args) > 0:
            raise ValueError("This Action have no arguments")
        return []


class InsertArgsParse:
    @staticmethod
    def args_validation(args: list[str]) -> list[int]:
        if len(args) != 1:
            raise ValueError(f"support only 1 arg")
        try:
            item = [int(args[0])]
            return item
        except ValueError:
            raise ValueError("Item should be an integer")


class MoveAdditionArgsParse:
    @staticmethod
    def args_validation(args: list[str]) -> list[int]:
        if len(args) != 2:
            raise ValueError(f"require only 2 args")
        try:
            parsed_args = [int(args[0]), int(args[1])]
            return parsed_args
        except ValueError:
            raise ValueError("Args should be an integer")


@ACTIONS_REGISTRY.register("FrontInsert")
class FrontInsert(InsertArgsParse, Action):
    def __init__(self, item: int):
        self.item = item

    def standard_func(self, collection: MutableSequence[int]) -> None:
        collection.insert(0, self.item)

    def redo_func(self, collection: MutableSequence[int]) -> None:
        collection.pop(0)


@ACTIONS_REGISTRY.register("BackInsert")
class BackInsert(InsertArgsParse, Action):
    def __init__(self, item: int):
        self.item = item

    def standard_func(self, collection: MutableSequence[int]) -> None:
        collection.append(self.item)

    def redo_func(self, collection: MutableSequence[int]) -> None:
        collection.pop(-1)


@ACTIONS_REGISTRY.register("Move")
class Move(MoveAdditionArgsParse, Action):
    def __init__(self, index_one: int, index_two: int):
        self.index_one = index_one
        self.index_two = index_two

    def standard_func(self, collection: MutableSequence[int]) -> None:
        self.validation(collection)
        first_elem = collection.pop(self.index_one)
        second_elem = collection.pop(self.index_two - 1)
        collection.insert(self.index_one, second_elem)
        collection.insert(self.index_two, first_elem)

    def redo_func(self, collection: MutableSequence[int]) -> None:
        self.validation(collection)
        self.standard_func(collection)

    def validation(self, collection: MutableSequence[int]) -> None:
        if len(collection) < 2:
            raise ValueError("Collection must contain more than 1 element")
        if self.index_one not in range(len(collection)):
            raise IndexError("First index out of range")
        if self.index_two not in range(len(collection)):
            raise IndexError("Second index out of range")
        if self.index_one > self.index_two:
            self.index_one, self.index_two = self.index_two, self.index_one


@ACTIONS_REGISTRY.register("Addition")
class Addition(MoveAdditionArgsParse, Action):
    def __init__(self, index: int, value: int):
        self.index = index
        self.value = value

    def standard_func(self, collection: MutableSequence[int]) -> None:
        self.validation(collection)
        collection[self.index] += self.value

    def redo_func(self, collection: MutableSequence[int]) -> None:
        self.validation(collection)
        collection[self.index] -= self.value

    def validation(self, collection: MutableSequence[int]) -> None:
        if self.index not in range(-len(collection), len(collection)):
            raise IndexError("Index out of range")


@ACTIONS_REGISTRY.register("Reverse")
class Reverse(NoArgsActionParse, Action):
    def standard_func(self, collection: MutableSequence[int]) -> None:
        collection.reverse()

    def redo_func(self, collection: MutableSequence[int]) -> None:
        collection.reverse()


@ACTIONS_REGISTRY.register("Multiply")
class Multiply(MoveAdditionArgsParse, Action):
    def __init__(self, index: int, value: int) -> None:
        self.index = index
        self.value = value
        self.original_value = 0

    def standard_func(self, collection: MutableSequence[int]) -> None:
        self.original_value = collection[self.index]
        collection[self.index] *= self.value

    def redo_func(self, collection: MutableSequence[int]) -> None:
        collection[self.index] = self.original_value

    def validation(self, collection: MutableSequence[int]) -> None:
        if self.index not in range(len(collection)):
            raise IndexError("Index out of range")


@ACTIONS_REGISTRY.register("FrontDelete")
class FrontDelete(NoArgsActionParse, Action):
    def __init__(self) -> None:
        self.original_value = 0

    def standard_func(self, collection: MutableSequence[int]) -> None:
        self.validation(collection)
        self.original_value = collection.pop(0)

    def redo_func(self, collection: MutableSequence[int]) -> None:
        collection.insert(0, self.original_value)

    def validation(self, collection: MutableSequence[int]) -> None:
        if len(collection) == 0:
            raise ValueError("Collection is empty")


@ACTIONS_REGISTRY.register("BackDelete")
class BackDelete(NoArgsActionParse, Action):
    def __init__(self) -> None:
        self.original_value = 0

    def standard_func(self, collection: MutableSequence[int]) -> None:
        self.validation(collection)
        self.original_value = collection.pop(-1)

    def redo_func(self, collection: MutableSequence[int]) -> None:
        collection.insert(len(collection), self.original_value)

    def validation(self, collection: MutableSequence[int]) -> None:
        if len(collection) == 0:
            raise ValueError("Collection is empty")


@ACTIONS_REGISTRY.register("SignChange")
class SignChange(NoArgsActionParse, Action):
    def standard_func(self, collection: MutableSequence[int]) -> None:
        for i in range(len(collection)):
            collection[i] *= -1

    def redo_func(self, collection: MutableSequence[int]) -> None:
        for i in range(len(collection)):
            collection[i] *= -1


@ACTIONS_REGISTRY.register("TransitElement")
class TransitElement(MoveAdditionArgsParse, Action):
    def __init__(self, pos_of_element: int, new_pos: int) -> None:
        self.pos_of_element = pos_of_element
        self.new_pos = new_pos

    def standard_func(self, collection: MutableSequence[int]) -> None:
        self.validation(collection)
        element = collection.pop(self.pos_of_element)
        collection.insert(self.new_pos, element)

    def redo_func(self, collection: MutableSequence[int]) -> None:
        element = collection.pop(self.new_pos)
        collection.insert(self.pos_of_element, element)

    def validation(self, collection: MutableSequence[int]) -> None:
        if len(collection) < 1:
            raise ValueError("Collection must contain 1 or more elements")
        if self.pos_of_element not in range(len(collection)):
            raise IndexError("First index out of range")
        if self.new_pos not in range(len(collection)):
            raise IndexError("Second index out of range")


@ACTIONS_REGISTRY.register("SumAdd")
class SumAdd(NoArgsActionParse, Action):
    def standard_func(self, collection: MutableSequence[int]) -> None:
        self.validation(collection)
        sum_of_elements = sum(collection)
        collection.append(sum_of_elements)

    def redo_func(self, collection: MutableSequence[int]) -> None:
        collection.pop(-1)

    def validation(self, collection: MutableSequence[int]) -> None:
        if len(collection) == 0:
            raise ValueError("Collection is empty")


class PCS:
    def __init__(self, collection: MutableSequence[int]) -> None:
        if not isinstance(collection, MutableSequence):
            raise NotSupportedCollectionTypeError(type(collection).__name__)
        self.actions: list[Action] = []
        self.collection = collection

    def apply(self, action: Action) -> None:
        action.standard_func(self.collection)
        self.actions.append(action)

    def redo(self) -> None:
        if len(self.collection) == 0:
            raise EmptyActionListError()
        action = self.actions.pop(-1)
        action.redo_func(self.collection)
