import asyncio
from tkinter import Tk

from bash import Model
from viewmodel import ViewModel


class App:
    MAX_QUOTES = 10

    def __init__(self) -> None:
        self.root = self._setup_root()
        self.model = Model(self.MAX_QUOTES, "https://башорг.рф/")

    def _setup_root(self) -> Tk:
        root = Tk()
        root.grid_columnconfigure(0, weight=1)
        root.grid_rowconfigure(0, weight=1)
        return root

    async def show(self) -> None:
        while True:
            self.root.update()
            await asyncio.sleep(0)

    async def start(self) -> None:
        viewmodel = ViewModel(self.model, self.root, asyncio.get_event_loop(), self.MAX_QUOTES)
        viewmodel.start()
        await self.show()


if __name__ == "__main__":
    app = App()
    asyncio.run(app.start())
