import pytest

from python_fma import (
    DivByZeroException,
    InexactException,
    InvalidException,
    OverflowException,
    UnderflowException,
    exception_compiled,
    round_mode_compiled,
    round_mode_supported,
)


class TestQueryFunctions:
    def test_exception_compiled_returns_bool(self):
        for name in (
            InvalidException,
            DivByZeroException,
            OverflowException,
            UnderflowException,
            InexactException,
        ):
            result = exception_compiled(name)
            assert isinstance(result, bool)

    def test_exception_compiled_invalid_name(self):
        class FakeException(Exception):
            pass

        with pytest.raises(ValueError, match="unknown exception"):
            exception_compiled(FakeException)  # pyright: ignore[reportArgumentType]

    def test_round_mode_compiled_returns_bool(self):
        for name in ("FE_TONEAREST", "FE_UPWARD", "FE_DOWNWARD", "FE_TOWARDZERO"):
            result = round_mode_compiled(name)
            assert isinstance(result, bool)

    def test_round_mode_compiled_invalid_name(self):
        with pytest.raises(ValueError, match="unknown rounding mode"):
            round_mode_compiled("FE_NOSUCH")  # pyright: ignore[reportArgumentType]

    def test_round_mode_supported_returns_bool(self):
        for name in ("FE_TONEAREST", "FE_UPWARD", "FE_DOWNWARD", "FE_TOWARDZERO"):
            result = round_mode_supported(name)
            assert isinstance(result, bool)

    def test_round_mode_supported_invalid_name(self):
        with pytest.raises(ValueError, match="unknown rounding mode"):
            round_mode_supported("FE_NOSUCH")  # pyright: ignore[reportArgumentType]
