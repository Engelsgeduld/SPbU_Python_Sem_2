from io import StringIO

import pytest

from src.homeworks.homework_3.task_1.main import *


class TestMain:
    @pytest.mark.parametrize(
        "user_input, expected_output",
        [
            ("BackDelete", "Collection is empty\n"),
            ("FrontDelete", "Collection is empty\n"),
            ("Multiply 1 3", "list index out of range\n"),
            ("Addition 1 2", "Index out of range\n"),
            ("Move 0 0", "Collection must contain more than 1 element\n"),
            ("Redo", "Actions list is empty. Nothing to redo\n"),
            ("111", "111 is not implemented\n"),
            ("Reverse 1 1", "This Action have no arguments\n"),
            ("BackInsert a", "Item should be an integer\n"),
            ("FrontInsert 1 1", "support only 1 arg\n"),
        ],
    )
    def test_action_exception(self, monkeypatch, user_input, expected_output):
        main_module = Main()
        monkeypatch.setattr("builtins.input", lambda _: user_input)
        fake_output = StringIO()
        monkeypatch.setattr("sys.stderr", fake_output)
        main_module.user_commands_fill()
        main_module.menu_handler()
        output = fake_output.getvalue()
        assert output == expected_output
