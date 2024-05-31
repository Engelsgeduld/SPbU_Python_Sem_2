from typing import Any, Callable, Optional

import numpy as np
import numpy.typing as tpg

from src.homeworks.homework_6.task_1.observer import Observable


class Player:
    def __init__(self, name: str, player_type: int, sign: int) -> None:
        self.name = name
        self.player_type = player_type
        self.sign = sign

    def move(self, *args: Any) -> Any:
        pass


class RandomBot(Player):
    def __init__(self, name: str, sign: int) -> None:
        super().__init__(name, 0, sign)

    def move(self, field: tpg.NDArray) -> Optional[tpg.ArrayLike]:
        available_moves = np.argwhere(field == 0)
        if len(available_moves) == 0:
            return None
        index = np.random.randint(0, len(available_moves))
        return available_moves[index]


class RealPlayer(Player):
    def __init__(self, name: str, sign: int) -> None:
        super().__init__(name, 1, sign)
        self.indexes = (-1, -1)

    def move(self) -> tuple[int, int]:
        return self.indexes

    def set_indexes(self, indexes: tuple[int, int]) -> None:
        self.indexes = indexes


class BeastPlayer(Player):
    def __init__(self, name: str, sign: int) -> None:
        super().__init__(name, 0, sign)

    @staticmethod
    def _available_moves(field: tpg.NDArray) -> list:
        return list(np.argwhere(field == 0))

    def _evaluate(self, field: tpg.NDArray) -> int:
        sums = [*np.sum(field, axis=0)] + [*np.sum(field, axis=1)] + [np.trace(field)] + [np.trace(np.rot90(field))]
        if (-1) * self.sign * len(field) in sums:
            return -10
        if self.sign * len(field) in sums:
            return 10
        return 0

    def _minimax(self, field: tpg.NDArray, depth: int, is_max: bool) -> int:
        score = self._evaluate(field)
        if score in (10, -10):
            return score
        if len(self._available_moves(field)) == 0:
            return 0
        if is_max:
            best = -1000
            for move in self._available_moves(field):
                field[move[0]][move[1]] += self.sign
                best = max(best, self._minimax(field, depth + 1, not is_max))
                field[move[0]][move[1]] = 0
        else:
            best = 1000
            for move in self._available_moves(field):
                field[move[0]][move[1]] += self.sign * (-1)
                best = min(best, self._minimax(field, depth + 1, not is_max))
                field[move[0]][move[1]] = 0
        return best

    def move(self, field: tpg.NDArray) -> tuple[int, int]:
        best_val = -1000
        best_move = (-1, -1)
        for move in self._available_moves(field):
            field[move[0]][move[1]] += self.sign
            move_val = self._minimax(field, 0, False)
            field[move[0]][move[1]] = 0
            if move_val > best_val:
                best_move = move
                best_val = move_val
        return best_move


class Game:
    def __init__(self, length: int, players: tuple[Player, Player]) -> None:
        self.session = Observable((-1, -1))
        self.length = length
        self.field = np.zeros(shape=(length, length))
        self.players = players
        self.current_player = self.players[0]
        self.game_status: Observable[Player | int | None] = Observable(1)

    def eog_check(self) -> None:
        sums = (
            [*np.sum(self.field, axis=0)]
            + [*np.sum(self.field, axis=1)]
            + [np.trace(self.field)]
            + [np.trace(np.rot90(self.field))]
        )
        if self.players[0].sign * self.length in sums:
            self.game_status.value = self.players[0]
        if self.players[1].sign * self.length in sums:
            self.game_status.value = self.players[1]
        if len(np.argwhere(self.field == 0)) == 0:
            self.game_status.value = None

    def correct_move_check(self, indexes: tuple[int, int]) -> bool:
        if self.field[indexes[0]][indexes[1]] != 0:
            return False
        return True

    def do_move(self) -> None:
        current_player = self.current_player
        if current_player.player_type == 1:
            move = current_player.move()
            correct = self.correct_move_check(move)
            if not correct:
                return
        else:
            move = current_player.move(self.field)
            if move is None:
                return
        self.field[move[0]][move[1]] = current_player.sign
        self.current_player = self.players[0] if current_player != self.players[0] else self.players[1]
        self.session.value = (current_player.sign, move)
        self.eog_check()

    def add_listener(self, func: Callable) -> None:
        self.session.add_callback(func)
