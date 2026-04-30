import ctypes as ct

import pytest

from python_fma import UnsupportedRoundingModeError, fma, round_mode_compiled, round_mode_supported


class TestFmaRoundingModes:
    def test_all_rounding_modes_accept_exact_fma(self):
        """Exact FMA results are the same regardless of rounding mode."""
        for mode in ("FE_TONEAREST", "FE_UPWARD", "FE_DOWNWARD", "FE_TOWARDZERO"):
            r = fma(ct.c_double(2.0), ct.c_double(3.0), ct.c_double(1.0), mode)
            assert r.value == 7.0

    def test_invalid_rounding_mode_name(self):
        with pytest.raises(ValueError, match="unknown rounding mode"):
            fma(ct.c_double(1.0), ct.c_double(2.0), ct.c_double(3.0), round="FE_NOSUCH")  # pyright: ignore[reportArgumentType]

    def test_unsupported_rounding_mode_raises(self):
        mode = "FE_UPWARD"
        if not round_mode_compiled(mode):
            pytest.skip(f"{mode} not compiled")
        if round_mode_supported(mode):
            pytest.skip(f"{mode} is supported on this platform")

        with pytest.raises(UnsupportedRoundingModeError):
            fma(ct.c_double(1.0), ct.c_double(2.0), ct.c_double(3.0), round=mode)
