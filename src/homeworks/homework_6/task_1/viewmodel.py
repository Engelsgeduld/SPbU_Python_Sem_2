import abc
from tkinter import Tk, ttk
from typing import Any, Optional

from src.homeworks.homework_1.task_1.registry import Registry
from src.homeworks.homework_6.task_1.model import BeastPlayer, Game, Player, RandomBot, RealPlayer
from src.homeworks.homework_6.task_1.view import (
    EndGameView,
    FieldView,
    LocalMultiplayerChoiceView,
    MainView,
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


Models_Register = Registry[IViewModel]()


class ViewModelSwapMixin:

    _root: Tk
    current_view: Optional[ttk.Frame] = None

    def swap(self, name: str, data: Any) -> None:
        if ViewModelSwapMixin.current_view is not None:
            ViewModelSwapMixin.current_view.destroy()
        ViewModelSwapMixin.current_view = Models_Register.dispatch(name)(*data).start()
        ViewModelSwapMixin.current_view.grid()


@Models_Register.register("Field")
class FieldViewModel(ViewModelSwapMixin, IViewModel):
    def __init__(self, root: Tk, players: tuple[Player, Player], length: int = 3):
        self._model = Game(3, players)
        self._root = root
        self._length = length

    def _bind(self, view: FieldView) -> None:
        self._model.game_status.add_callback(lambda winner: self.swap("End", [self._root, winner]))
        self._model.add_listener(lambda value: self.move_callback(view, value))
        if self._model.current_player.player_type == 0:
            self._model.do_move()
        for row in range(self._length):
            for col in range(self._length):
                view.buttons[row][col].config(command=(lambda row_i=row, col_i=col: self.button_request(row_i, col_i))) #type: ignore
        view.new_game_button.config(command=lambda: self.swap("Main", [self._root]))

    def button_request(self, row: int, col: int) -> None:
        current_player = self._model.current_player
        if current_player.player_type == 1 and hasattr(current_player, "set_indexes"):
            current_player.set_indexes((row, col))
            self._model.do_move()

    def move_callback(self, view: FieldView, value: tuple[int, tuple[int, int]]) -> None:
        view.button_apply(*value)
        if self._model.current_player.player_type == 0:
            self._model.do_move()

    def start(self) -> FieldView:
        frame = FieldView(self._root, self._length)
        self._bind(frame)
        return frame


@Models_Register.register("Main")
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


@Models_Register.register("SinglePlayer")
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


@Models_Register.register("Multiplayer")
class MultiplayerViewModel(ViewModelSwapMixin, IViewModel):
    def __init__(self, root: Tk) -> None:
        self._root = root

    def _bind(self, view: MultiplayerView) -> None:
        view.local.config(command=lambda: self.swap("MChoice", [self._root]))

    def start(self) -> MultiplayerView:
        frame = MultiplayerView(self._root)
        self._bind(frame)
        return frame


@Models_Register.register("End")
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


@Models_Register.register("SChoice")
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


@Models_Register.register("MChoice")
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
