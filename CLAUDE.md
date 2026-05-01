# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project State

This is a working Python/C FMA binding module with full test coverage. It uses
Python 3.10+ with a virtual environment at `.venv/`.

## Project Goal

This is a FMA binding module from C to Python. Python provides native FMA in
`math.fma`, but it lacks support for 32bit float, and user can not set rounding
mode. This project fixes these limitations. 

## Project API and Implementation Details

This project provides an interface: 

```python
import ctypes as ct
from typing import Literal

ct_float = ct.c_double | ct.c_float
round_mode = Literal["FE_TONEAREST", "FE_UPWARD", "FE_DOWNWARD", "FE_TOWARDZERO"]

def fma(x: ct_float, y: ct_float, z: ct_float, round:round_mode | None = None, unsuppressed_exception: set[type[FloatException]] = set(DivByZeroException, OverflowException)) -> ct_float
```

- When float operation exception (divide-by-zero, overflow, underflow, inexact, invalid) happens, corresponing Exception is thrown. 
- If the round mode is not supported by current implementation, an exception is thrown. 
- If the input x, y and z is not the same type, an exception is thrown.
- The original round mode is recovered afte this FMA operation. 

## Python Environment

- Python 3.13.5
- Virtual environment: `.venv/` (activate with `source .venv/bin/activate`)
- Install packages with `pip install <package>`

## Conventions

Once the project has code, follow these conventions by default unless a specific tool/pattern is established:

- **Type hints**: Use Python 3.10 style type hints everywhere new code is added. The code must be fully type-hinted, and `any` should be avoied when possible. Do not use str when Literal is suitable and possible. Do not duplicate Literals everywhere when it is suitable and possible to write it as one global variable.
- **Testing**: Use `pytest` for tests
- **Formatting/linting**: Use `ruff` for both formatting and linting, and use `pyright` strict mode to check types.
- **Import sorting**: Use `ruff check --select I --fix` for import sorting
- **Project structure**: Use src convension
- **C code**: Use C11 standard. Please read manuals about `fma` and `fenv` for the C API used. Use `#ifdef FE_*` preprocessor guards to detect rounding mode and FP exception availability at compile time.
- **CMake code**: Use CMake to manage C code. Keep CMakeLists.txt minimal — just `add_library`, link `m` on non-Windows, add compiler FP flags (`/fp:strict` for MSVC, `-frounding-math -fsignaling-nans` for Clang/GCC), and `install`.
- **C cinding**: Use `Ctypes` to do C binding. the C code must be formatted by `clang-format-22` with `./.clang-format` config.
- **CI**: A dockerfile to build this project without Python ABI compatibility (i.e. `wheel.py-api = "py3"`) in manylinux2014, manylinux_2_28, manylinux_2_34, use `auditwheel` to produced universal package. The output binary file should be in `./wheelhouse` folder. Do not automatically run docker, due to limited disk space. Use Github CI file to build this project and run test on Win, Mac and Linux, and also generate coverage badge. Make the compiled `.whl` file an artifact in Github CI.