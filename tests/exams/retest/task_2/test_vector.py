from random import randint

import hypothesis.strategies as st
import numpy as np
import pytest
from hypothesis import given

from src.exams.retest.task_2.vector import EqualError, Vector, VectorLengthError


class TestVector:
    @given(st.integers(min_value=1, max_value=1000))
    def test_zero(self, grange):
        vector = Vector([0 for _ in range(grange)])
        assert vector.is_zero()

    @given(st.integers(min_value=1, max_value=1000))
    def test_equal(self, grange):
        coords = [randint(-1000, 1000) for _ in range(grange)]
        assert Vector(coords) == Vector(coords)

    @given(st.integers(min_value=1, max_value=1000))
    def test_scalar_mul_func(self, grange):
        first_coords = [randint(-1000, 1000) for _ in range(grange)]
        second_coords = [randint(-1000, 1000) for _ in range(grange)]
        result = Vector(first_coords) * Vector(second_coords)
        expected = np.dot(np.array(first_coords), np.array(second_coords))
        assert result == expected

    @given(st.integers(min_value=100, max_value=1000))
    def test_vector_mul_func(self, grange):
        first_coords = [randint(-1000, 1000) for _ in range(3)]
        second_coords = [randint(-1000, 1000) for _ in range(3)]
        expected = Vector(list(np.cross(first_coords, second_coords)))
        result = Vector(first_coords) @ Vector(second_coords)
        assert expected == result

    @given(st.integers(min_value=100, max_value=1000))
    def test_add_func(self, grange):
        first_coords = [randint(-1000, 1000) for _ in range(grange)]
        second_coords = [randint(-1000, 1000) for _ in range(grange)]
        result = Vector(first_coords) + Vector(second_coords)
        expected = Vector(list(np.array(first_coords) + np.array(second_coords)))
        assert result == expected

    @given(st.integers(min_value=100, max_value=1000))
    def test_sub_func(self, grange):
        first_coords = [randint(-1000, 1000) for _ in range(grange)]
        second_coords = [randint(-1000, 1000) for _ in range(grange)]
        result = Vector(first_coords) - Vector(second_coords)
        expected = Vector(list(np.array(first_coords) - np.array(second_coords)))
        assert result == expected


class TestExceptions:
    @given(st.integers(min_value=100, max_value=1000))
    def test_length_exception(self, grange):
        f_vector = Vector([randint(-10, 10) for _ in range(randint(1, 100))])
        s_vector = Vector([randint(-10, 10) for _ in range(randint(101, 1000))])
        with pytest.raises(VectorLengthError):
            Vector._len_check(f_vector, s_vector)

    @pytest.mark.parametrize("values", [([], (), []), ("a", "b", "c"), (3, 4, None)])
    def test_init_exception(self, values):
        with pytest.raises(TypeError):
            vector = Vector(values)

    @pytest.mark.parametrize("smth", [[], (), {}, 54])
    def test_equal_exception(self, smth):
        vector = Vector([1, 2, 3])
        with pytest.raises(EqualError):
            res = vector == smth

    def test_vector_mul_exception(self):
        vector = Vector([1, 2, 3, 4])
        with pytest.raises(VectorLengthError):
            res = vector @ vector
