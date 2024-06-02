import socket
from typing import Any, Callable, Optional

import numpy as np
import numpy.typing as tpg
from loguru import logger

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

    def move(self, field: tpg.NDArray) -> tuple[Optional[tpg.ArrayLike], int]:
        available_moves = np.argwhere(field == 0)
        if len(available_moves) == 0:
            return None, self.sign
        index = np.random.randint(0, len(available_moves))
        return available_moves[index], self.sign


class OnlinePlayer(Player):
    def __init__(self, name: str, sign: int) -> None:
        super().__init__(name, 2, sign)
        self.indexes = (-1, -1)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def set_indexes(self, indexes: tuple[int, int]) -> None:
        self.indexes = indexes

    def connect(self, ip: str, port: int, command: str, name: str) -> None:
        self.sock.connect((ip, port))
        self.sock.sendall(f"{command},{name},{self.sign}".encode())
        status = self.sock.recv(1024).decode()
        if status != "202":
            raise ValueError("202")

    def get_sign(self) -> None:
        data = self.sock.recv(1024).decode()
        print(data)
        self.sign = int(data)

    def close_conn(self) -> None:
        self.sock.close()

    def move(self) -> tuple[Optional[tuple[int, int]], int]:
        self.sock.send(f"{self.indexes[0]},{self.indexes[1]},{self.sign},{self.sock.getsockname()[1]}".encode())
        return self.indexes, self.sign

    def listen_mode(self) -> tuple[tuple[int, int], int]:
        print(2)
        message = self.sock.recv(1024).decode()
        data = message.split(",")
        first_index, second_index, sign = data
        return (int(first_index), int(second_index)), int(sign)


class RealPlayer(Player):
    def __init__(self, name: str, sign: int) -> None:
        super().__init__(name, 1, sign)
        self.indexes = (-1, -1)

    def move(self) -> tuple[tuple[int, int], int]:
        return self.indexes, self.sign

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

    def move(self, field: tpg.NDArray) -> tuple[tuple[int, int], int]:
        best_val = -1000
        best_move = (-1, -1)
        for move in self._available_moves(field):
            field[move[0]][move[1]] += self.sign
            move_val = self._minimax(field, 0, False)
            field[move[0]][move[1]] = 0
            if move_val > best_val:
                best_move = move
                best_val = move_val
        return best_move, self.sign


class Game:
    def __init__(self, length: int, players: tuple[Player, Player]) -> None:
        self.session = Observable((-1, -1))
        self.length = length
        self.field = np.zeros(shape=(length, length))
        self.players = players
        self.current_player = 0
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

    def check_move_correctness(self, indexes: tuple[int, int]) -> bool:
        return self.field[indexes[0]][indexes[1]] == 0

    def do_move(self, wait: bool = False) -> None:
        current_player = self.players[self.current_player]
        if current_player.player_type in (1, 2):
            if wait and hasattr(current_player, "listen_mode"):
                move, sign = current_player.listen_mode()
            else:
                move, sign = current_player.move()
        else:
            move, sign = current_player.move(self.field)
            if move is None:
                return
        if not self.check_move_correctness(move):
            logger.error("Wrong User move")
            return
        self.field[move[0]][move[1]] = sign
        self.current_player = 1 - self.current_player
        self.session.value = (sign, move)
        self.eog_check()

    def add_listener(self, func: Callable) -> None:
        self.session.add_callback(func)

    def get_current_player(self) -> Player:
        return self.players[self.current_player]
