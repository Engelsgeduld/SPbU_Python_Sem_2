import sys
from contextlib import contextmanager
from typing import Any, Generator, MutableSequence

from src.homeworks.homework_1.task_1.registry import Registry
from src.homeworks.homework_3.task_1.PerformedCommandStorage import ACTIONS_REGISTRY, PerformedCommandStorage
from src.homeworks.homework_3.task_1.StorageExceptions import NoImplementedActionError

MENU_LINE = "View - see available actions\nRedo - redo the action\nCollection - Current Collection View\nEXIT"


class Main:
    def __init__(self) -> None:
        self.user_commands = Registry[object]()
        self.actions = ACTIONS_REGISTRY
        self.collection: MutableSequence[int] = []
        self.pcs = PerformedCommandStorage(self.collection)

    @staticmethod
    @contextmanager
    def context_manager() -> Generator[Any, Any, None]:
        try:
            yield
        except Exception as error:
            print(error, file=sys.stderr)

    @staticmethod
    def input_parser(line: str) -> tuple[str, list[str]]:
        args = line.split(" ")
        return args[0], args[1:]

    def user_commands_fill(self) -> None:
        commands = {
            "View": lambda: print(*self.actions.register_of_names.keys(), sep=" "),
            "Redo": self.pcs.redo,
            "EXIT": lambda: exit(),
            "Collection": lambda: print(f"current_collection: {self.collection}"),
        }
        for command in commands:
            self.user_commands.register(command)(commands[command])

    def menu_handler(self) -> None:
        line = input("Enter Command and arguments\n")
        try:
            user_command = self.user_commands.dispatch(line)
            with self.context_manager():
                user_command()
        except ValueError:
            command, args = self.input_parser(line)
            with self.context_manager():
                try:
                    action = self.actions.dispatch(command)
                except ValueError:
                    raise NoImplementedActionError(command)
                implement_action = action.init_with_validation(args)
                self.pcs.apply(implement_action)

    def main_body(self) -> None:
        self.user_commands_fill()
        print(MENU_LINE)
        while True:
            self.menu_handler()


if __name__ == "__main__":
    main = Main()
    main.main_body()
