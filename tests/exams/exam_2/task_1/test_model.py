import pytest

from src.exams.exam_2.task_1.bash import Model


class TestModel:
    @pytest.mark.parametrize("request_num", ["byrating", "", "random"])
    def test_quote_count(self, request_num):
        model = Model(10, "https://башорг.рф/")
        result = model.parse_request(request_num)
        assert len(result) == 10

    @pytest.mark.parametrize("num_of_quotes", list(range(1, 26)))
    def test_len_of_request(self, num_of_quotes):
        model = Model(num_of_quotes, "https://башорг.рф/")
        result = model.parse_request("")
        assert len(result) == num_of_quotes

    @pytest.mark.parametrize("request_num", ["byrating", "", "random"])
    def test_type(self, request_num):
        model = Model(10, "https://башорг.рф/")
        result = model.parse_request(request_num)
        assert all([type(line) is str for line in result])


