import abc
from tkinter import Tk, ttk
from typing import Any, Optional

from src.homeworks.homework_1.task_1.registry import Registry
from src.homeworks.homework_6.task_1.model import BeastPlayer, Game, OnlinePlayer, Player, RandomBot, RealPlayer
from src.homeworks.homework_6.task_1.view import (
    CreateView,
    EndGameView,
    FieldView,
    LocalMultiplayerChoiceView,
    MainView,
    MultiplayerCommandView,
    MultiplayerView,
    SChoiceView,
    SinglePlayerView,
)


class IViewModel(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def __init__(self, *args: Any) -> None:
        pass

    @abc.abstractmethod
    def start(self) -> ttk.Frame:
        raise NotImplementedError


MODEL_REGISTRY = Registry[IViewModel]()


class ViewModelSwapMixin:
    _root: Tk
    current_view: Optional[ttk.Frame] = None

    def swap(self, name: str, data: Any) -> None:
        if ViewModelSwapMixin.current_view is not None:
            ViewModelSwapMixin.current_view.destroy()
        ViewModelSwapMixin.current_view = MODEL_REGISTRY.dispatch(name)(*data).start()
        ViewModelSwapMixin.current_view.grid()


@MODEL_REGISTRY.register("Field")
class FieldViewModel(ViewModelSwapMixin, IViewModel):
    def __init__(self, root: Tk, players: tuple[Player, Player], length: int = 3):
        self._model = Game(3, players)
        self._root = root
        self._length = length

    def _bind(self, view: FieldView) -> None:
        self._model.game_status.add_callback(lambda winner: self.swap("End", [self._root, winner]))
        self._model.add_listener(lambda value: self.move_callback(view, value))
        current_player = self._model.get_current_player()
        if current_player.player_type == 0:
            self._model.do_move()
        for row in range(self._length):
            for col in range(self._length):
                view.buttons[row][col].config(command=(lambda row_i=row, col_i=col: self.button_request(row_i, col_i)))  # type: ignore
        view.new_game_button.config(command=lambda: self.swap("Main", [self._root]))
        if current_player.player_type == 2 and current_player.sign == -1:
            self._model.do_move(True)

    def button_request(self, row: int, col: int) -> None:
        current_player = self._model.get_current_player()
        if current_player.player_type in (1, 2) and hasattr(current_player, "set_indexes"):
            current_player.set_indexes((row, col))
            self._model.do_move()

    def move_callback(self, view: FieldView, value: tuple[int, tuple[int, int]]) -> None:
        view.button_apply(*value)
        current_player = self._model.get_current_player()
        if current_player.player_type == 0:
            self._model.do_move()
        if current_player.player_type == 2 and self._model.current_player == 1 and current_player.sign == 1:
            self._model.do_move(True)
        if current_player.player_type == 2 and self._model.current_player == 0 and current_player.sign == -1:
            self._model.do_move(True)

    def start(self) -> FieldView:
        frame = FieldView(self._root, self._length)
        self._bind(frame)
        return frame


@MODEL_REGISTRY.register("Main")
class MainViewModel(ViewModelSwapMixin, IViewModel):
    def __init__(self, root: Tk) -> None:
        self._root = root

    def _bind(self, view: MainView) -> None:
        view.single_player_button.config(command=lambda: self.swap("SinglePlayer", [self._root]))
        view.multiplayer_button.config(command=lambda: self.swap("Multiplayer", [self._root]))

    def start(self) -> MainView:
        self._root.update()
        frame = MainView(self._root)
        self._bind(frame)
        frame.grid()
        ViewModelSwapMixin.current_view = frame
        return frame


@MODEL_REGISTRY.register("SinglePlayer")
class SinglePlayerViewModel(ViewModelSwapMixin, IViewModel):
    def __init__(self, root: Tk) -> None:
        self._root = root

    def _bind(self, view: SinglePlayerView) -> None:
        view.easy_bot_button.config(command=lambda: self.swap("SChoice", (self._root, 0)))
        view.hard_button.config(command=lambda: self.swap("SChoice", (self._root, 1)))

    def start(self) -> SinglePlayerView:
        frame = SinglePlayerView(self._root)
        self._bind(frame)
        return frame


@MODEL_REGISTRY.register("Multiplayer")
class MultiplayerViewModel(ViewModelSwapMixin, IViewModel):
    def __init__(self, root: Tk) -> None:
        self._root = root

    def _bind(self, view: MultiplayerView) -> None:
        view.local.config(command=lambda: self.swap("MChoice", [self._root]))
        view.online.config(command=lambda: self.swap("Commands", [self._root]))

    def start(self) -> MultiplayerView:
        frame = MultiplayerView(self._root)
        self._bind(frame)
        return frame


@MODEL_REGISTRY.register("End")
class EndGameViewModel(ViewModelSwapMixin, IViewModel):
    def __init__(self, root: Tk, player: Player):
        self._root = root
        self._name = player.name if player else None

    def _bind(self, view: EndGameView) -> None:
        view.new_game_button.config(command=lambda: self.end_game(view))

    def start(self) -> EndGameView:
        self._root.update()
        frame = EndGameView(self._root, self._name)
        self._bind(frame)
        return frame

    def end_game(self, view: EndGameView) -> None:
        view.new_game_button.destroy()
        self.swap("Main", [self._root])


@MODEL_REGISTRY.register("SChoice")
class ChoiceViewModel(ViewModelSwapMixin, IViewModel):
    def __init__(self, root: Tk, mode: int) -> None:
        self._root = root
        self._mode = mode

    def _bind(self, view: SChoiceView) -> None:
        view.first_choice_button.config(
            command=lambda: self.swap("Field", (self._root, self.game_config(view.name_entry.get(), self._mode, 1)))
        )
        view.second_choice_button.config(
            command=lambda: self.swap("Field", (self._root, self.game_config(view.name_entry.get(), self._mode, -1)))
        )

    def game_config(self, name: str, mode: int, number: int) -> tuple[Player, Player]:
        player = RealPlayer(name, number)
        bot = BeastPlayer("Beast", -number) if mode else RandomBot("Noob", -number)
        return (player, bot) if number == 1 else (bot, player)

    def start(self) -> SChoiceView:
        frame = SChoiceView(self._root)
        self._bind(frame)
        return frame


@MODEL_REGISTRY.register("MChoice")
class LocalMultiplayerChoiceViewModel(ViewModelSwapMixin, IViewModel):
    def __init__(self, root: Tk) -> None:
        self._root = root

    def _bind(self, view: LocalMultiplayerChoiceView) -> None:
        view.first_choice_button.config(
            command=lambda: self.swap(
                "Field", (self._root, self.game_config((view.first_name_entry.get(), view.second_name_entry.get()), 1))
            )
        )
        view.second_choice_button.config(
            command=lambda: self.swap(
                "Field", (self._root, self.game_config((view.first_name_entry.get(), view.second_name_entry.get()), -1))
            )
        )

    def game_config(self, names: tuple[str, str], number: int) -> tuple[Player, Player]:
        players = RealPlayer(names[0], number), RealPlayer(names[1], -number)
        return players if number == 1 else players[::-1]

    def start(self) -> LocalMultiplayerChoiceView:
        frame = LocalMultiplayerChoiceView(self._root)
        self._bind(frame)
        return frame


@MODEL_REGISTRY.register("Commands")
class MultiplayerCommandViewModel(ViewModelSwapMixin, IViewModel):
    def __init__(self, root: Tk) -> None:
        self._root = root

    def _bind(self, view: MultiplayerCommandView) -> None:
        view.create_button.config(command=lambda: self.swap("Connect", [self._root, *self.get_input(view)]))
        view.connect_button.config(command=lambda: self.create_config(*self.get_input(view)))

    def create_config(self, ip: str, port: int, name: str) -> None:
        player = OnlinePlayer("You", -1)
        player.connect(ip, port, "2", name)
        player.get_sign()
        self.swap("Field", [self._root, (player, player)])

    def start(self) -> MultiplayerCommandView:
        frame = MultiplayerCommandView(self._root)
        self._bind(frame)
        return frame

    @staticmethod
    def get_input(view: MultiplayerCommandView) -> tuple[str, int, str]:
        ip, port = view.ip_entry.get().split(":")
        name = view.room_name_entry.get()
        return ip, int(port), name


@MODEL_REGISTRY.register("Connect")
class CreateViewModel(ViewModelSwapMixin, IViewModel):
    def __init__(self, root: Tk, ip: str, port: int, name: str) -> None:
        self._root = root
        self._ip = ip
        self._port = port
        self._name = name

    def _bind(self, view: CreateView) -> None:
        view.first_choice_button.config(command=lambda: self.create_config(1))
        view.second_choice_button.config(command=lambda: self.create_config(-1))

    def create_config(self, sign: int) -> None:
        player = OnlinePlayer("name_2", sign)
        player.connect(self._ip, self._port, "1", self._name)
        player.get_sign()
        self.swap("Field", [self._root, (player, player)])

    def start(self) -> CreateView:
        frame = CreateView(self._root)
        self._bind(frame)
        return frame
