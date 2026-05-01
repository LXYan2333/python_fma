from __future__ import annotations

import ctypes as ct
from typing import Literal

from python_fma._binding import lib as _lib

__all__: list[str] = [
    "exception_compiled",
    "fma",
    "FloatException",
    "DivByZeroException",
    "FeatureNotCompiledError",
    "InexactException",
    "InvalidException",
    "OverflowException",
    "round_mode_compiled",
    "round_mode_supported",
    "UnderflowException",
    "UnsupportedRoundingModeError",
]

_FMA_DYNAMIC = -1

_ROUND_MODE_MAP: dict[RoundMode, int] = {
    "FE_TONEAREST": 0,
    "FE_UPWARD": 1,
    "FE_DOWNWARD": 2,
    "FE_TOWARDZERO": 3,
}


class FloatException(Exception):
    """Base for all floating-point operation exceptions."""


class DivByZeroException(FloatException):
    """The divide-by-zero exception occurs when an operation on finite numbers
    produces infinity as exact answer."""


class InexactException(FloatException):
    """The inexact exception occurs when the rounded result of an operation is
    not equal to the infinite precision result."""


class InvalidException(FloatException):
    """The invalid exception occurs when there is no well-defined result for an
    operation, as for 0/0 or infinity - infinity or sqrt(-1)."""


class OverflowException(FloatException):
    """The overflow exception occurs when a result has to be represented as a
    floating-point number, but has (much) larger absolute value than the largest
    (finite) floating-point number that is representable."""


class UnderflowException(FloatException):
    """The underflow exception occurs when a result has to be represented as a
    floating-point number, but has smaller absolute value than the smallest
    positive normalized floating-point number (and would lose much accuracy when
    represented as a denormalized number)."""


class UnsupportedRoundingModeError(FloatException, ValueError):
    """The requested rounding mode is not available on this platform."""


class FeatureNotCompiledError(FloatException):
    """A floating-point exception or rounding mode is not supported by the
    current build (compile-time detection from ``<fenv.h>``)."""


CtFloat = ct.c_double | ct.c_float
RoundMode = Literal["FE_TONEAREST", "FE_UPWARD", "FE_DOWNWARD", "FE_TOWARDZERO"]

_EXC_TYPE_MAP: dict[type[FloatException], int] = {
    InvalidException: 0,
    DivByZeroException: 1,
    OverflowException: 2,
    UnderflowException: 3,
    InexactException: 4,
}


def exception_compiled(name: type[FloatException]) -> bool:
    """Return whether detection of the floating-point exception *name* is
    available in the C build.

    Parameters
    ----------
    name : FloatException subclass
        One of ``InvalidException``, ``DivByZeroException``, ``OverflowException``,
        ``UnderflowException``, or ``InexactException``.

    Returns
    -------
    bool
        ``True`` if the exception is available in this build, ``False``
        otherwise (i.e. the host system's ``<fenv.h>`` does not define the
        corresponding macro).

    Raises
    ------
    ValueError
        *name* is not a recognised exception class.
    """
    try:
        exc_type = _EXC_TYPE_MAP[name]
    except KeyError:
        raise ValueError(
            f"unknown exception: {name} (expected one of {set(_EXC_TYPE_MAP)})"
        ) from None
    return _lib.fma_exception_compiled(exc_type)


def round_mode_compiled(name: RoundMode) -> bool:
    """Return whether the rounding mode *name* was detected at compile time.

    Parameters
    ----------
    name : RoundMode
        One of ``"FE_TONEAREST"``, ``"FE_UPWARD"``, ``"FE_DOWNWARD"``,
        or ``"FE_TOWARDZERO"``.

    Returns
    -------
    bool
        ``True`` if the rounding mode is available in this build, ``False``
        otherwise (i.e. the host system's ``<fenv.h>`` does not define the
        corresponding macro).

    Raises
    ------
    ValueError
        *name* is not a recognised rounding-mode string.
    """
    try:
        mode = _ROUND_MODE_MAP[name]
    except KeyError:
        raise ValueError(
            f"unknown rounding mode: {name!r} (expected one of {set(_ROUND_MODE_MAP)})"
        ) from None
    return _lib.fma_round_mode_compiled(mode)


def round_mode_supported(name: RoundMode) -> bool:
    """Return whether the rounding mode *name* is supported at runtime.

    Parameters
    ----------
    name : RoundMode

    Returns
    -------
    bool
        ``True`` if the rounding mode is supported at runtime on this
        platform, ``False`` otherwise.

    Raises
    ------
    ValueError
        *name* is not a recognised rounding-mode string.
    """
    try:
        mode = _ROUND_MODE_MAP[name]
    except KeyError:
        raise ValueError(
            f"unknown rounding mode: {name!r} (expected one of {set(_ROUND_MODE_MAP)})"
        ) from None
    return _lib.fma_round_mode_supported(mode)


def fma(
    x: CtFloat,
    y: CtFloat,
    z: CtFloat,
    round: RoundMode | None = None,
    unsuppressed_exception: set[type[FloatException]] = {DivByZeroException, OverflowException},
) -> CtFloat:
    """Compute ``x * y + z`` with a single rounding (fused multiply-add).

    Parameters
    ----------
    x, y, z: ctypes.c_double or ctypes.c_float
        Operands.  All three must be the **same** ctypes numeric type.
    round: str or None
        Rounding mode.  ``None`` leaves the current FP rounding mode
        unchanged.  Accepted values:

        - ``"FE_TONEAREST"`` — round to nearest, ties to even
        - ``"FE_UPWARD"`` — round toward +infinity
        - ``"FE_DOWNWARD"`` — round toward -infinity
        - ``"FE_TOWARDZERO"`` — truncate toward zero
    unsuppressed_exception: set of FloatException subclasses
        Set of floating-point exception types that are allowed to propagate.
        Any exception not in this set is silently suppressed.
        Default is ``{DivByZeroException, OverflowException}``.

    Returns
    -------
    ctypes.c_double or ctypes.c_float
        The FMA result, in the same type as the inputs.

    Raises
    ------
    TypeError
        *x*, *y*, and *z* are not all the same type, or not a supported type.
    ValueError
        *round* is not a recognised rounding-mode string.
    FeatureNotCompiledError
        The requested rounding mode or an exception flag is not available in
        this build (the host system's ``<fenv.h>`` does not define the
        corresponding macro).
    UnsupportedRoundingModeError
        The platform does not support the requested rounding mode.
    InvalidException
        The invalid exception occurs when there is no well-defined result
        for an operation, as for 0/0 or infinity - infinity or sqrt(-1).
    DivByZeroException
        The divide-by-zero exception occurs when an operation on finite
        numbers produces infinity as exact answer.
    OverflowException
        The overflow exception occurs when a result has to be represented
        as a floating-point number, but has (much) larger absolute value
        than the largest (finite) floating-point number that is representable.
    UnderflowException
        The underflow exception occurs when a result has to be represented
        as a floating-point number, but has smaller absolute value than the
        smallest positive normalized floating-point number (and would lose
        much accuracy when represented as a denormalized number).
    InexactException
        The inexact exception occurs when the rounded result of an operation
        is not equal to the infinite precision result.  It may occur whenever
        overflow or underflow occurs.
    """
    t = type(x)
    if type(y) is not t or type(z) is not t:
        raise TypeError(
            f"x, y, z must all be the same type "
            f"(got {type(x).__name__}, {type(y).__name__}, {type(z).__name__})"
        )
    if t not in (ct.c_double, ct.c_float):
        raise TypeError(f"expected ct.c_double or ct.c_float, got {t.__name__}")

    round_mode: int
    if round is None:
        round_mode = _FMA_DYNAMIC
    else:
        try:
            round_mode = _ROUND_MODE_MAP[round]
        except KeyError:
            raise ValueError(
                f"unknown rounding mode: {round!r} (expected one of {set(_ROUND_MODE_MAP)})"
            ) from None
        if not _lib.fma_round_mode_compiled(round_mode):
            raise FeatureNotCompiledError(
                f"rounding mode {round!r} is not available in this build"
            )
        if not _lib.fma_round_mode_supported(round_mode):
            raise UnsupportedRoundingModeError(
                f"rounding mode {round!r} is not supported on this platform"
            )

    exc_invalid = ct.c_bool(False)
    exc_divbyzero = ct.c_bool(False)
    exc_overflow = ct.c_bool(False)
    exc_underflow = ct.c_bool(False)
    exc_inexact = ct.c_bool(False)

    if t is ct.c_double:
        result = _lib.fma_double(
            x,
            y,
            z,
            round_mode,
            ct.byref(exc_invalid),
            ct.byref(exc_divbyzero),
            ct.byref(exc_overflow),
            ct.byref(exc_underflow),
            ct.byref(exc_inexact),
        )
        result_type: type[CtFloat] = ct.c_double
    else:
        result = _lib.fma_float(
            x,
            y,
            z,
            round_mode,
            ct.byref(exc_invalid),
            ct.byref(exc_divbyzero),
            ct.byref(exc_overflow),
            ct.byref(exc_underflow),
            ct.byref(exc_inexact),
        )
        result_type = ct.c_float

    exc_map: list[tuple[ct.c_bool, type[FloatException]]] = [
        (exc_invalid, InvalidException),
        (exc_divbyzero, DivByZeroException),
        (exc_overflow, OverflowException),
        (exc_underflow, UnderflowException),
        (exc_inexact, InexactException),
    ]
    for flag, exc_cls in exc_map:
        if flag.value:
            if exc_cls in unsuppressed_exception:
                raise exc_cls(f"floating-point exception: {exc_cls.__name__}")

    return result_type(result)
