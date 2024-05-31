from tkinter import Tk

from viewmodel import MainViewModel


class App:
    APPLICATION_NAME = "Tic-Tac-Toe"
    START_SIZE = 512, 512
    MIN_SIZE = 256, 256

    def __init__(self) -> None:
        self._root = self._setup_root()
        self._viewmodel = MainViewModel(self._root)

    def _setup_root(self) -> Tk:
        root = Tk()
        root.geometry("x".join(map(str, self.START_SIZE)))
        root.minsize(*self.MIN_SIZE)
        root.title(self.APPLICATION_NAME)
        root.grid_columnconfigure(0, weight=1)
        root.grid_rowconfigure(0, weight=1)
        return root

    def start(self) -> None:
        self._viewmodel.start()
        self._root.mainloop()


if __name__ == "__main__":
    App().start()
