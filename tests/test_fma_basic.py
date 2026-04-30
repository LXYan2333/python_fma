import ctypes as ct

import pytest

from python_fma import fma


class TestFmaBasic:
    def test_double_fma(self):
        r = fma(ct.c_double(2.0), ct.c_double(3.0), ct.c_double(1.0))
        assert r.value == 7.0
        assert type(r) is ct.c_double

    def test_float_fma(self):
        r = fma(ct.c_float(2.0), ct.c_float(3.0), ct.c_float(1.0))
        assert r.value == 7.0
        assert type(r) is ct.c_float

    def test_negative_values(self):
        r = fma(ct.c_double(-2.0), ct.c_double(3.0), ct.c_double(1.0))
        assert r.value == -5.0

    def test_zero_operands(self):
        r = fma(ct.c_double(0.0), ct.c_double(5.0), ct.c_double(3.0))
        assert r.value == 3.0

    def test_round_none_is_default(self):
        r = fma(ct.c_double(2.0), ct.c_double(3.0), ct.c_double(1.0), round=None)
        assert r.value == 7.0


class TestFmaTypeValidation:
    def test_mismatched_types(self):
        with pytest.raises(TypeError, match="same type"):
            fma(ct.c_double(1.0), ct.c_float(2.0), ct.c_double(3.0))

    def test_unsupported_type(self):
        with pytest.raises(TypeError, match="expected ct.c_double or ct.c_float"):
            fma(
                ct.c_int(1),  # pyright: ignore[reportArgumentType]
                ct.c_int(2),  # pyright: ignore[reportArgumentType]
                ct.c_int(3),  # pyright: ignore[reportArgumentType]
            )

    def test_two_floats_one_double(self):
        with pytest.raises(TypeError, match="same type"):
            fma(ct.c_float(1.0), ct.c_float(2.0), ct.c_double(3.0))

    def test_all_same_type_passes(self):
        r = fma(ct.c_double(1.0), ct.c_double(2.0), ct.c_double(3.0))
        assert r.value == 5.0
