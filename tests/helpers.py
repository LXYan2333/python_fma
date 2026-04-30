import ctypes as ct


def bits_to_double(bits: str) -> ct.c_double:
    """Convert a binary string to a ``ct.c_double`` via bit-cast.

    ``bits`` must contain only ``"0"`` and ``"1"`` and is interpreted as the
    64-bit IEEE 754 representation (sign | exponent | mantissa).
    """
    return ct.c_double.from_buffer(ct.c_uint64(int(bits, base=2)))


def bits_from_double(x: ct.c_double) -> str:
    """Return the 64-bit IEEE 754 representation of *x* as a binary string."""
    return f"{ct.c_uint64.from_buffer(x).value:064b}"


def bits_to_float(bits: str) -> ct.c_float:
    """Convert a binary string to a ``ct.c_float`` via bit-cast.

    ``bits`` must contain only ``"0"`` and ``"1"`` and is interpreted as the
    32-bit IEEE 754 representation (sign | exponent | mantissa).
    """
    return ct.c_float.from_buffer(ct.c_uint32(int(bits, base=2)))


def bits_from_float(x: ct.c_float) -> str:
    """Return the 32-bit IEEE 754 representation of *x* as a binary string."""
    return f"{ct.c_uint32.from_buffer(x).value:032b}"


def fma_double_raw(
    x: ct.c_double,
    y: ct.c_double,
    z: ct.c_double,
    round_mode: int,
) -> tuple[ct.c_double, list[str]]:
    """Call the C ``fma_double`` directly, bypassing the Python exception layer.

    Returns ``(result, active_exceptions)`` where *active_exceptions* is a list
    of exception flag names that were set by the operation.
    """
    from python_fma._binding import lib as _lib

    exc_invalid = ct.c_bool(False)
    exc_divbyzero = ct.c_bool(False)
    exc_overflow = ct.c_bool(False)
    exc_underflow = ct.c_bool(False)
    exc_inexact = ct.c_bool(False)

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

    flags: list[str] = []
    if exc_invalid.value:
        flags.append("FE_INVALID")
    if exc_divbyzero.value:
        flags.append("FE_DIVBYZERO")
    if exc_overflow.value:
        flags.append("FE_OVERFLOW")
    if exc_underflow.value:
        flags.append("FE_UNDERFLOW")
    if exc_inexact.value:
        flags.append("FE_INEXACT")

    return ct.c_double(result), flags


def fma_float_raw(
    x: ct.c_float,
    y: ct.c_float,
    z: ct.c_float,
    round_mode: int,
) -> tuple[ct.c_float, list[str]]:
    """Call the C ``fma_float`` directly, bypassing the Python exception layer.

    Returns ``(result, active_exceptions)`` where *active_exceptions* is a list
    of exception flag names that were set by the operation.
    """
    from python_fma._binding import lib as _lib

    exc_invalid = ct.c_bool(False)
    exc_divbyzero = ct.c_bool(False)
    exc_overflow = ct.c_bool(False)
    exc_underflow = ct.c_bool(False)
    exc_inexact = ct.c_bool(False)

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

    flags: list[str] = []
    if exc_invalid.value:
        flags.append("FE_INVALID")
    if exc_divbyzero.value:
        flags.append("FE_DIVBYZERO")
    if exc_overflow.value:
        flags.append("FE_OVERFLOW")
    if exc_underflow.value:
        flags.append("FE_UNDERFLOW")
    if exc_inexact.value:
        flags.append("FE_INEXACT")

    return ct.c_float(result), flags
