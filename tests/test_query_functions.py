import pytest

from python_fma import exception_compiled, round_mode_compiled, round_mode_supported


class TestQueryFunctions:
    def test_exception_compiled_returns_bool(self):
        for name in ("FE_INVALID", "FE_DIVBYZERO", "FE_OVERFLOW", "FE_UNDERFLOW", "FE_INEXACT"):
            result = exception_compiled(name)
            assert isinstance(result, bool)

    def test_exception_compiled_invalid_name(self):
        with pytest.raises(ValueError, match="unknown exception"):
            exception_compiled("FE_NOSUCH")

    def test_round_mode_compiled_returns_bool(self):
        for name in ("FE_TONEAREST", "FE_UPWARD", "FE_DOWNWARD", "FE_TOWARDZERO"):
            result = round_mode_compiled(name)
            assert isinstance(result, bool)

    def test_round_mode_compiled_invalid_name(self):
        with pytest.raises(ValueError, match="unknown rounding mode"):
            round_mode_compiled("FE_NOSUCH")

    def test_round_mode_supported_returns_bool(self):
        for name in ("FE_TONEAREST", "FE_UPWARD", "FE_DOWNWARD", "FE_TOWARDZERO"):
            result = round_mode_supported(name)
            assert isinstance(result, bool)

    def test_round_mode_supported_invalid_name(self):
        with pytest.raises(ValueError, match="unknown rounding mode"):
            round_mode_supported("FE_NOSUCH")
