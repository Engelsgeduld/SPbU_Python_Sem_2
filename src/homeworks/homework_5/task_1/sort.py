import os.path
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from math import ceil
from random import randint
from timeit import timeit
from typing import Callable

import matplotlib.pyplot as plt


class Model:
    def merge_sort(self, lst: list[int]) -> list[int]:
        if len(lst) <= 1:
            return lst
        middle = len(lst) // 2
        left = self.merge_sort(lst[:middle])
        right = self.merge_sort(lst[middle:])
        return self.merge([left, right])

    @staticmethod
    def merge(lst: list[list[int]]) -> list[int]:
        if len(lst) != 2:
            raise ValueError("Merge require 2 data sets")
        left, right = lst
        result = []
        while left and right:
            if left[0] < right[0]:
                result.append(left[0])
                left.pop(0)
            else:
                result.append(right[0])
                right.pop(0)
        if left:
            result += left
        if right:
            result += right
        return result

    def parallel_merge_sort(self, data: list[int], threads_count: int, pool_executor: Callable) -> list[int]:
        if threads_count <= 0:
            raise ValueError("Threads/Process count should be positive")
        size = ceil(len(data) / threads_count)
        data_parts = [data[i * size : (i + 1) * size] for i in range(threads_count)]
        with pool_executor(max_workers=threads_count) as executor:
            sorted_data = list(executor.map(self.merge_sort, data_parts))
            while len(sorted_data) > 1:
                extra = sorted_data.pop() if len(sorted_data) % 2 == 1 else None
                sorted_data = [(sorted_data[i], sorted_data[i + 1]) for i in range(0, len(sorted_data), 2)]
                sorted_data = list(executor.map(self.merge, sorted_data)) + ([extra] if extra else [])
        return sorted_data[0]

    def parallel_sort_time(self, data: list[int], threads_count: int, multiprocessing: bool = False) -> float:
        executor = ProcessPoolExecutor if multiprocessing else ThreadPoolExecutor
        return timeit(lambda: self.parallel_merge_sort(data, threads_count, executor), number=100)

    def base_sort_time(self, data: list[int]) -> float:
        return timeit(lambda: self.merge_sort(data), number=100)


class Printer:
    @staticmethod
    def create_figure(
        th_counts: list[int], data_set_len: int, data_sets: list[list[float]], names: list[str], file_path: str
    ) -> None:
        if len(data_sets) != len(names):
            raise ValueError("Number of names should be equal to length of dataset")
        fig, ax = plt.subplots()
        for i in range(len(data_sets)):
            ax.plot(th_counts, data_sets[i], label=names[i])
        ax.set(xlabel="threads/process", ylabel="time")
        ax.grid()
        ax.legend()
        plt.title(label=f"dataset length: {data_set_len}, threads/process count: {th_counts}")
        fig.savefig(f"{file_path}.png")
        plt.show()


class Main:
    @staticmethod
    def script(len_data: int, data: list[int], threads: list[int], output_path: str) -> None:
        if os.path.exists(f"{output_path}.png"):
            raise ValueError(f"Output file ({output_path}) already exists")
        printer = Printer()
        model = Model()
        mult_pros_data = [model.parallel_sort_time(data, thread, True) for thread in threads]
        thread_data = [model.parallel_sort_time(data, thread) for thread in threads]
        basic_data = [model.base_sort_time(data)] * len(threads)
        data_sets = [mult_pros_data, thread_data, basic_data]
        printer.create_figure(threads, len_data, data_sets, ["multiprocessing", "threading", "BASE"], output_path)


if __name__ == "__main__":
    main = Main()
    len_data = 100_000
    threads = list(range(1, 9))
    data = [randint(-100, 100) for _ in range(len_data)]
    main.script(len_data, data, threads, "result_release")