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

- **Type hints**: Use Python 3.10 style type hints everywhere new code is added. The code must be fully type-hinted, and `any` should be avoied when possible.
- **Testing**: Use `pytest` for tests
- **Formatting/linting**: Use `ruff` for both formatting and linting, and use `pyright` strict mode to check types.
- **Import sorting**: Use `ruff check --select I --fix` for import sorting
- **Project structure**: Use src convension
- **C code**: Use C11 standard. Please read manuals about `fma` and `fenv` for the C API used.
- **CMake code**: Use CMake to manage C code, and use `try_compile` to check whether these rounding mode and float point exception is supported by current implementation. A `test_exception_round_support.h.in` in `./cmake` with `#cmakedefine01` to reflect exception and round support is configured to a header file under `${CMAKE_CURRENT_BUILD_DIRECTORY}` for c code to report unsupported exception and round mode. Use `target_sources` to add `PUBLIC` header file to the target, and use `target_include_directory` to add PRIVATE and test result headers.
- **C cinding**: Use `Ctypes` to do C binding. the C code must be formatted by `/usr/bin/clang-format-22` with `./.clang-format` config.
- **CI**: A dockerfile to build this project with `ABI3` in manylinux2014, manylinux_2_28, manylinux_2_34. Do not automatically run docker, due to limited disk space. Please add a Github CI file to build them. the output binary file should be in `./wheelhouse` folder.