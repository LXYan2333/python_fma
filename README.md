# python-fma

![coverage](badges/coverage.svg)

A Python **fused multiply-add** (FMA) binding with **32 and 64-bit float** support and
**configurable IEEE 754 rounding modes**.

Python 3.13+ provides `math.fma`, but it operates on `float` (IEEE 754 double)
only and does not expose the rounding direction. This module fills both gaps:

- Accepts `ct.c_double` (float64) **and** `ct.c_float` (float32).
- Lets the caller select the rounding mode per-call.
- Detects and reports IEEE 754 floating-point exceptions (invalid, overflow,
  underflow, inexact, divide-by-zero).
- Restores the original FP rounding state after each operation.

## Note

I write this project with vibe coding, but I carefully read every line in `/src/` and `/csrc/` folder, and I glanced at test code (and provides some data for rounding test), so the core logic should be ok.

The coverage test rate is high, and all non-platform-dependent code is covered in test.

---

## Installation

```console
$ pip install python-fma
``` 

The package ships a pre-built wheel for Linux, Windows and MacOS, support x86 and ARM architecture.

### Requirements

- Python >= 3.10

if you want to build from source:

- C11 compiler
- CMake >= 3.15

---

## API

### `fma(x, y, z, round=None, unsuppressed_exception=...)`

```python
import ctypes as ct

from python_fma import fma, DivByZeroException, OverflowException

r = fma(ct.c_double(2.0), ct.c_double(3.0), ct.c_double(1.0))
# r.value == 7.0
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `x, y, z` | `ct.c_double` or `ct.c_float` | – | Operands (must all be the same type) |
| `round` | `str` or `None` | `None` | Rounding mode (see below). `None` leaves the current FP mode unchanged. |
| `unsuppressed_exception` | `set` of exception classes | `{DivByZeroException, OverflowException}` | Exception types allowed to propagate; all others are silently suppressed. |

**Rounding mode strings:**

| Name | Behaviour |
|------|-----------|
| `"FE_TONEAREST"` | Round to nearest, ties to even |
| `"FE_UPWARD"` | Round toward +infinity |
| `"FE_DOWNWARD"` | Round toward -infinity |
| `"FE_TOWARDZERO"` | Truncate toward zero |

**Returns:** `ct.c_double` or `ct.c_float` (same type as the inputs).

**Raises:**
- `TypeError` — inputs are not all the same type or not a supported type.
- `ValueError` — unrecognised rounding-mode string.
- `FeatureNotCompiledError` — the rounding mode or an exception flag was not
  detected at compile time.
- `UnsupportedRoundingModeError` — the platform does not support the requested
  rounding mode at runtime.
- `DivByZeroException`, `OverflowException` — by default; other exceptions
  (`InvalidException`, `UnderflowException`, `InexactException`) are suppressed
  unless explicitly included in `unsuppressed_exception`.

### `exception_compiled(name)`

Return whether detection of the floating-point exception `name` is available in
the C build.

```python
from python_fma import exception_compiled

exception_compiled("FE_INVALID")   # True / False
exception_compiled("FE_NOSUCH")    # ValueError
```

### `round_mode_compiled(name)`

Return whether the rounding mode `name` was detected at compile time.

```python
from python_fma import round_mode_compiled

round_mode_compiled("FE_UPWARD")   # True / False
```

### `round_mode_supported(name)`

Return whether the rounding mode `name` is supported at runtime.

```python
from python_fma import round_mode_supported

round_mode_supported("FE_TOWARDZERO")   # True / False
```

---

## Exception hierarchy

```
Exception
  └── FloatException
        ├── InvalidException          (FE_INVALID)
        ├── DivByZeroException        (FE_DIVBYZERO)
        ├── OverflowException         (FE_OVERFLOW)
        ├── UnderflowException        (FE_UNDERFLOW)
        ├── InexactException          (FE_INEXACT)
        ├── FeatureNotCompiledError   (query/compile-time support)
        └── UnsupportedRoundingModeError  (also a ValueError)
```

---

## Usage examples

### Basic FMA

```python
import ctypes as ct
from python_fma import fma

r = fma(ct.c_double(2.0), ct.c_double(3.0), ct.c_double(1.0))
# 2.0 * 3.0 + 1.0 = 7.0
```

### Single-precision FMA

```python
r = fma(ct.c_float(1.5), ct.c_float(2.0), ct.c_float(0.5))
# r.value == 3.5, type(r) is ct.c_float
```

### Explicit rounding mode

```python
r = fma(ct.c_double(1.0), ct.c_double(1.0), ct.c_double(0.1),
        round="FE_UPWARD")
```

### Controlling which exceptions propagate

```python
# Only allow InvalidException to propagate; suppress everything else.
r = fma(ct.c_double(float("inf")), ct.c_double(0.0), ct.c_double(0.0),
        unsuppressed_exception={InvalidException})
```

### Querying compile-time feature support

```python
from python_fma import exception_compiled, round_mode_compiled

if not round_mode_compiled("FE_UPWARD"):
    print("FE_UPWARD not available in this build")
```

---

## Development

### Setup

```console
$ python -m venv .venv
$ source .venv/bin/activate
$ pip install -e .
```

### Lint and type-check

```console
$ ruff check src/ tests/
$ ruff format --check src/ tests/
$ npx pyright src/ tests/
```

### Test

```console
$ python -m pytest tests/ -v
```

### Build a wheel

```console
$ pip install build
$ python -m build
```

### CI / Docker build

Manylinux wheels are built via Docker:

```console
$ docker build \
  --build-arg BASE_IMAGE=quay.io/pypa/manylinux2014_x86_64 \
  -t builder .
$ docker run --rm -v "$PWD/wheelhouse:/wheelhouse" builder
```

Windows and macOS wheels are built natively on GitHub Actions runners. See
`.github/workflows/build.yml` for the full CI matrix.

---

## Project structure

```
python-fma/
├── csrc/                  # C source (fma_module.c, fma_module.h, CMakeLists.txt)
├── src/
│   └── python_fma/
│       ├── __init__.py    # Public Python API
│       └── _binding.py    # ctypes bindings to the C library
├── badges/                # generated coverage badge
├── tests/                 # pytest test suite
├── pyproject.toml         # Build configuration (scikit-build-core, ruff)
├── README.md              # This file
├── Dockerfile             # manylinux wheel builder
└── .github/workflows/     # CI workflows
```

---

## License

MPL
