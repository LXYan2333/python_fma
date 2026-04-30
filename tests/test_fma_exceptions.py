import ctypes as ct

import pytest

from python_fma import (
    InexactException,
    InvalidException,
    OverflowException,
    UnderflowException,
    exception_compiled,
    fma,
)


class TestFmaExceptions:
    def test_invalid_operation(self):
        with pytest.raises(InvalidException, match="InvalidException"):
            fma(
                ct.c_double(float("inf")),
                ct.c_double(0.0),
                ct.c_double(0.0),
                unsuppressed_exception={InvalidException},
            )

    def test_overflow_double(self):
        with pytest.raises(OverflowException, match="OverflowException"):
            fma(ct.c_double(1e200), ct.c_double(1e200), ct.c_double(0.0))

    def test_overflow_float(self):
        with pytest.raises(OverflowException, match="OverflowException"):
            fma(ct.c_float(1e20), ct.c_float(1e20), ct.c_float(0.0))

    @pytest.mark.skipif(
        not exception_compiled("FE_UNDERFLOW"),
        reason="FE_UNDERFLOW not compiled",
    )
    def test_underflow_double(self):
        with pytest.raises(UnderflowException, match="UnderflowException"):
            fma(
                ct.c_double(2.0 ** (-600)),
                ct.c_double(2.0 ** (-600)),
                ct.c_double(0.0),
                unsuppressed_exception={UnderflowException},
            )

    @pytest.mark.skipif(
        not exception_compiled("FE_UNDERFLOW"),
        reason="FE_UNDERFLOW not compiled",
    )
    def test_underflow_float(self):
        with pytest.raises(UnderflowException, match="UnderflowException"):
            fma(
                ct.c_float(2.0 ** (-80)),
                ct.c_float(2.0 ** (-80)),
                ct.c_float(0.0),
                unsuppressed_exception={UnderflowException},
            )

    def test_inexact(self):
        with pytest.raises(InexactException, match="InexactException"):
            fma(
                ct.c_double(1.0),
                ct.c_double(1.0),
                ct.c_double(0.1),
                unsuppressed_exception={InexactException},
            )

    def test_invalid_exception_takes_priority(self):
        with pytest.raises(InvalidException):
            fma(
                ct.c_double(float("inf")),
                ct.c_double(0.0),
                ct.c_double(float("inf")),
                unsuppressed_exception={InvalidException},
            )


class TestFmaUnsuppressedException:
    def test_default_suppresses_inexact(self):
        r = fma(ct.c_double(1.0), ct.c_double(1.0), ct.c_double(0.1))
        assert isinstance(r, ct.c_double)
        assert r.value == 1.1

    def test_default_suppresses_invalid(self):
        r = fma(ct.c_double(float("inf")), ct.c_double(0.0), ct.c_double(0.0))
        assert isinstance(r, ct.c_double)

    @pytest.mark.skipif(
        not exception_compiled("FE_UNDERFLOW"),
        reason="FE_UNDERFLOW not compiled",
    )
    def test_default_suppresses_underflow(self):
        r = fma(ct.c_double(2.0 ** (-600)), ct.c_double(2.0 ** (-600)), ct.c_double(0.0))
        assert isinstance(r, ct.c_double)

    def test_empty_set_suppresses_all(self):
        r = fma(
            ct.c_double(float("inf")),
            ct.c_double(0.0),
            ct.c_double(0.0),
            unsuppressed_exception=set(),
        )
        assert isinstance(r, ct.c_double)

    def test_unsuppressed_inexact_still_raises(self):
        with pytest.raises(InexactException):
            fma(
                ct.c_double(1.0),
                ct.c_double(1.0),
                ct.c_double(0.1),
                unsuppressed_exception={InexactException},
            )

    def test_unsuppressed_overflow_raises(self):
        with pytest.raises(OverflowException):
            fma(
                ct.c_double(1e200),
                ct.c_double(1e200),
                ct.c_double(0.0),
                unsuppressed_exception={OverflowException},
            )
