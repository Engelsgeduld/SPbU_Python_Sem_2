import tempfile

import hypothesis.strategies as st
import pytest
from click.testing import CliRunner
from hypothesis import given

from src.homeworks.homework_5.task_1.sort import *


class TestModel:
    @given(st.integers(min_value=1, max_value=8))
    def test_parallel_sort(self, threads):
        model = Model()
        data = [randint(-100, 100) for _ in range(10000)]
        expected = sorted(data)
        assert model.parallel_merge_sort(data, threads) == expected
        assert model.parallel_merge_sort(data, threads, True) == expected

    @given(st.integers(min_value=1, max_value=8))
    def test_another_parallel_sort(self, threads):
        model = Model()
        data = [randint(-100, 100) for _ in range(10000)]
        expected = sorted(data)
        assert model.another_parallel_merge_sort(threads, data) == expected

    @pytest.mark.parametrize("threads", [-3, 0, -1])
    def test_parallel_sort_exception(self, threads):
        model = Model()
        with pytest.raises(ValueError):
            model.parallel_merge_sort([1, 2, 3], threads)

    @pytest.mark.parametrize("lst", [([[1, 2, 3]]), ([[1, 2], [1, 2, 3], [1, 2]]), ([[]])])
    def test_merge_exception(self, lst):
        model = Model()
        with pytest.raises(ValueError):
            model.merge(lst)


class TestPrinter:
    def test_names_length(self):
        printer = Printer()
        with pytest.raises(ValueError):
            printer.create_figure([1, 2, 3], 2, [[1, 2], [1, 2]], ["a", "b", "c"], "result")


class TestMain:
    def test_main_file_exception(self):
        runner = CliRunner()
        with tempfile.NamedTemporaryFile(suffix=".png") as file:
            path = file.name.replace(".png", "")
            result = runner.invoke(start, ["2", "5", path])
            assert result.exit_code == 1
