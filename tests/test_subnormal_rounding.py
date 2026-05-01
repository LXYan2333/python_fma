import ctypes as ct

import pytest
from python_fma import _ROUND_MODE_MAP
from tests.helpers import (
    bits_to_double,
    bits_to_float,
    fma_double_raw,
    fma_float_raw,
)


class TestSubnormalRoundingDouble:
    _SIGN = 2**63

    @pytest.mark.parametrize(
        ("multiplier", "expected_bits"),
        [
            # 1.5 * 2^(-1074) is exactly halfway between 2^(-1074) (bit=1)
            # and 2^(-1073) (bit=2).  Ties-to-even picks the even mantissa.
            (
                1.5,
                {
                    "FE_TONEAREST": 2,
                    "FE_UPWARD": 2,
                    "FE_DOWNWARD": 1,
                    "FE_TOWARDZERO": 1,
                },
            ),
            # 0.75 * 2^(-1074) is closer to 2^(-1074) than to 0.
            (
                0.75,
                {
                    "FE_TONEAREST": 1,
                    "FE_UPWARD": 1,
                    "FE_DOWNWARD": 0,
                    "FE_TOWARDZERO": 0,
                },
            ),
            # 2.0 * 2^(-1074) = 2^(-1073) is exactly representable.
            (
                2.0,
                {
                    "FE_TONEAREST": 2,
                    "FE_UPWARD": 2,
                    "FE_DOWNWARD": 2,
                    "FE_TOWARDZERO": 2,
                },
            ),
            # -1.5 * 2^(-1074): negative halfway case.
            # Ties-to-even picks mantissa=2 (sign bit set).
            (
                -1.5,
                {
                    "FE_TONEAREST": _SIGN + 2,
                    "FE_UPWARD": _SIGN + 1,
                    "FE_DOWNWARD": _SIGN + 2,
                    "FE_TOWARDZERO": _SIGN + 1,
                },
            ),
            # -0.75 * 2^(-1074): closer to -2^(-1074) than to 0.
            # FE_UPWARD and FE_TOWARDZERO give -0.0 (sign bit set),
            # matching platform FMA zero-sign behavior.
            (
                -0.75,
                {
                    "FE_TONEAREST": _SIGN + 1,
                    "FE_UPWARD": _SIGN,
                    "FE_DOWNWARD": _SIGN + 1,
                    "FE_TOWARDZERO": _SIGN,
                },
            ),
            # -2.0 * 2^(-1074) = -2^(-1073), exactly representable.
            (
                -2.0,
                {
                    "FE_TONEAREST": _SIGN + 2,
                    "FE_UPWARD": _SIGN + 2,
                    "FE_DOWNWARD": _SIGN + 2,
                    "FE_TOWARDZERO": _SIGN + 2,
                },
            ),
        ],
    )
    def test_subnormal_rounding(self, multiplier: float, expected_bits: dict[str, int]) -> None:
        small = bits_to_double("1")  # smallest subnormal, 2^(-1074)
        mul = ct.c_double(multiplier)
        zero = ct.c_double(0.0)

        for mode_name, expected in expected_bits.items():
            result, flags = fma_double_raw(small, mul, zero, _ROUND_MODE_MAP[mode_name])
            result_bits = ct.c_uint64.from_buffer(result).value
            assert result_bits == expected, (
                f"fma({multiplier}g, 2^(-1074), 0) with {mode_name}: "
                f"expected bit pattern {expected}, got {result_bits} "
                f"(flags: {flags})"
            )


class TestSubnormalRoundingFloat:
    _SIGN = 2**31

    @pytest.mark.parametrize(
        ("multiplier", "expected_bits"),
        [
            (
                1.5,
                {
                    "FE_TONEAREST": 2,
                    "FE_UPWARD": 2,
                    "FE_DOWNWARD": 1,
                    "FE_TOWARDZERO": 1,
                },
            ),
            (
                0.75,
                {
                    "FE_TONEAREST": 1,
                    "FE_UPWARD": 1,
                    "FE_DOWNWARD": 0,
                    "FE_TOWARDZERO": 0,
                },
            ),
            (
                2.0,
                {
                    "FE_TONEAREST": 2,
                    "FE_UPWARD": 2,
                    "FE_DOWNWARD": 2,
                    "FE_TOWARDZERO": 2,
                },
            ),
            (
                -1.5,
                {
                    "FE_TONEAREST": _SIGN + 2,
                    "FE_UPWARD": _SIGN + 1,
                    "FE_DOWNWARD": _SIGN + 2,
                    "FE_TOWARDZERO": _SIGN + 1,
                },
            ),
            (
                -0.75,
                {
                    "FE_TONEAREST": _SIGN + 1,
                    "FE_UPWARD": _SIGN,
                    "FE_DOWNWARD": _SIGN + 1,
                    "FE_TOWARDZERO": _SIGN,
                },
            ),
            (
                -2.0,
                {
                    "FE_TONEAREST": _SIGN + 2,
                    "FE_UPWARD": _SIGN + 2,
                    "FE_DOWNWARD": _SIGN + 2,
                    "FE_TOWARDZERO": _SIGN + 2,
                },
            ),
        ],
    )
    def test_subnormal_rounding_float(
        self,
        multiplier: float,
        expected_bits: dict[str, int],
    ) -> None:
        small = bits_to_float("1")  # smallest float subnormal, 2^(-149)
        mul = ct.c_float(multiplier)
        zero = ct.c_float(0.0)

        for mode_name, expected in expected_bits.items():
            result, flags = fma_float_raw(small, mul, zero, _ROUND_MODE_MAP[mode_name])
            result_bits = ct.c_uint32.from_buffer(result).value
            assert result_bits == expected, (
                f"fma({multiplier}g, 2^(-149), 0) with {mode_name}: "
                f"expected bit pattern {expected}, got {result_bits} "
                f"(flags: {flags})"
            )
