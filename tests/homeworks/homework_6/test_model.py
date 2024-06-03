import pytest

from src.homeworks.homework_6.task_1.model import *


class TestBasicFuncs:
    @pytest.mark.parametrize("execution_number", range(100))
    def test_eof_func(self, execution_number):
        players = RandomBot("bot", 1), RandomBot("bot", -1)
        game = Game(3, players)
        for _ in range(3 * 3):
            game.do_move()
        assert game.game_status.value != 1

    def test_correct_move_func(self):
        players = RandomBot("bot", 1), RandomBot("bot", -1)
        game = Game(3, players)
        for _ in range(3 * 3):
            game.do_move()
        for i in range(3):
            for j in range(3):
                assert game.check_move_correctness((i, j)) == 0

    @pytest.mark.parametrize("execution_number", range(10))
    def test_beast_bot(self, execution_number):
        players = BeastPlayer("bot", 1), BeastPlayer("bot", -1)
        game = Game(3, players)
        for _ in range(3 * 3):
            game.do_move()
        assert game.game_status.value is None
