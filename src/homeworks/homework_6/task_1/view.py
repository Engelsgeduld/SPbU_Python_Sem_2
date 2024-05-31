from tkinter import *
from tkinter import ttk
from typing import Optional


class MainView(ttk.Frame):
    def __init__(self, root: Tk) -> None:
        super().__init__(root)

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

        self.single_player_button = ttk.Button(self, text="SinglePlayer")
        self.single_player_button.grid(row=1, column=1)

        self.multiplayer_button = ttk.Button(self, text="Multiplayer")
        self.multiplayer_button.grid(row=1, column=2)


class SinglePlayerView(ttk.Frame):
    def __init__(self, root: Tk) -> None:
        super().__init__(root)

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

        self.easy_bot_button = ttk.Button(self, text="EasyBot")
        self.easy_bot_button.grid(row=1, column=1)

        self.hard_button = ttk.Button(self, text="HardBot")
        self.hard_button.grid(row=1, column=2)


class MultiplayerView(ttk.Frame):
    def __init__(self, root: Tk) -> None:
        super().__init__(root)

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

        self.local = ttk.Button(self, text="LocalMultiplayer")
        self.local.grid(row=1, column=1)

        self.online = ttk.Button(self, text="OnlineMultiplayer")
        self.online.grid(row=1, column=2)


class FieldView(ttk.Frame):
    def __init__(self, root: Tk, length: int = 3) -> None:
        super().__init__(root)

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

        self.new_game_button = ttk.Button(self, text="New Game")
        self.new_game_button.grid(row=0, column=1, pady=10)

        self.buttons: list[list[ttk.Button]] = [[] for _ in range(length)]
        for row in range(1, length + 1):
            for col in range(length):
                self.buttons[row - 1].append(ttk.Button(self, text="", width=5))
                self.buttons[row - 1][col].grid(row=row, column=col, pady=2, padx=1)

    def button_apply(self, changer: int, indexes: tuple[int, int]) -> None:
        changer_icon = "X" if changer == 1 else "O"
        self.buttons[indexes[0]][indexes[1]].config(text=changer_icon)


class EndGameView(ttk.Frame):
    def __init__(self, root: Tk, name: Optional[str]) -> None:
        super().__init__(root)

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

        if name:
            self.winner_label = ttk.Label(self, text=f"Winner -- {name}")
        else:
            self.winner_label = ttk.Label(self, text=f"DRAW")
        self.winner_label.grid(row=0, column=1)
        self.new_game_button = ttk.Button(self, text="New Game")
        self.new_game_button.grid(row=1, column=1)


class SChoiceView(ttk.Frame):
    def __init__(self, root: Tk) -> None:
        super().__init__(root)

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

        self.first_choice_button = ttk.Button(self, text="First turn")
        self.first_choice_button.grid(row=3, column=0, pady=10)
        self.second_choice_button = ttk.Button(self, text="Second turn")
        self.second_choice_button.grid(row=3, column=2, pady=10)

        self.name_entry = ttk.Entry(self)
        self.name_entry.insert(0, "Enter nickname")
        self.name_entry.grid(row=1, column=1)


class LocalMultiplayerChoiceView(ttk.Frame):
    def __init__(self, root: Tk) -> None:
        super().__init__(root)

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

        self.first_choice_button = ttk.Button(self, text="Player 1 first")
        self.first_choice_button.grid(row=1, column=1)
        self.second_choice_button = ttk.Button(self, text="Player 2 first")
        self.second_choice_button.grid(row=1, column=2)

        self.first_name_entry = ttk.Entry(self)
        self.first_name_entry.insert(0, "Enter name of first player")
        self.first_name_entry.grid(row=0, column=1, padx=5)

        self.second_name_entry = ttk.Entry(self)
        self.second_name_entry.insert(0, "Enter name of first player")
        self.second_name_entry.grid(row=0, column=2, padx=5)
