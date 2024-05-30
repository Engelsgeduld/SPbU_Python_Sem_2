import asyncio
from tkinter import Tk

from src.exams.exam_2.task_1.bash import Model
from src.exams.exam_2.task_1.view import MainView


class ViewModel:
    def __init__(self, model: Model, root: Tk, loop: asyncio.AbstractEventLoop, number_of_quotes: int) -> None:
        self.number_of_quotes = number_of_quotes
        self.model = model
        self.root = root
        self.loop = loop

    def _bind(self, view: MainView) -> None:
        view.best_btn.config(command=lambda: self.loop.create_task(self.request_apply(view, 0)))
        view.new_btn.config(command=lambda: self.loop.create_task(self.request_apply(view, 1)))
        view.random_btn.config(command=lambda: self.loop.create_task(self.request_apply(view, 2)))

    async def request_apply(self, view: MainView, request: int) -> None:
        try:
            ready_text = ""
            text = await self.model.main(request)
            for quote in text:
                ready_text += quote
            view.set_message(ready_text)
        except Exception as e:
            view.set_message(repr(e))

    def start(self) -> MainView:
        frame = MainView(self.root)
        self._bind(frame)
        frame.pack()
        return frame
