"""Low-level ctypes bindings to the C libfma_module shared library.

This module is internal; all public APIs are exposed via
:mod:`python_fma.__init__`.
"""

from __future__ import annotations

import ctypes as ct
import importlib.util as _iu
import os
import sys

__all__: list[str] = []

_ext: str
# fmt: off
if sys.platform == "linux":
    _ext = ".so"
elif sys.platform == "darwin":          # pragma: no cover
    _ext = ".dylib"                     # pragma: no cover
elif sys.platform == "win32":           # pragma: no cover
    _ext = ".dll"                       # pragma: no cover
else:                                   # pragma: no cover
    raise ImportError(f"unsupported platform: {sys.platform}")
# fmt: on

_lib_name = f"libfma_module{_ext}"


def _find_library() -> str:
    """Locate the shared library, supporting both regular and editable installs."""
    # Ask the import system where python_fma lives.  For editable installs
    # scikit-build-core extends __path__ to include the site-packages
    # directory where the shared library is installed.
    _pkg_spec = _iu.find_spec("python_fma")
    if _pkg_spec is not None and _pkg_spec.submodule_search_locations:
        for _loc in _pkg_spec.submodule_search_locations:
            _candidate = os.path.join(_loc, _lib_name)
            if os.path.exists(_candidate):
                return _candidate

    # Fallback: alongside this file.
    return os.path.join(os.path.dirname(__file__), _lib_name)


_lib_path = _find_library()

lib = ct.CDLL(_lib_path)

lib.fma_double.argtypes = [
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_int,
    ct.POINTER(ct.c_bool),
    ct.POINTER(ct.c_bool),
    ct.POINTER(ct.c_bool),
    ct.POINTER(ct.c_bool),
    ct.POINTER(ct.c_bool),
]
lib.fma_double.restype = ct.c_double

lib.fma_float.argtypes = [
    ct.c_float,
    ct.c_float,
    ct.c_float,
    ct.c_int,
    ct.POINTER(ct.c_bool),
    ct.POINTER(ct.c_bool),
    ct.POINTER(ct.c_bool),
    ct.POINTER(ct.c_bool),
    ct.POINTER(ct.c_bool),
]
lib.fma_float.restype = ct.c_float

lib.fma_round_mode_supported.argtypes = [ct.c_int]
lib.fma_round_mode_supported.restype = ct.c_bool

lib.fma_round_mode_compiled.argtypes = [ct.c_int]
lib.fma_round_mode_compiled.restype = ct.c_bool

lib.fma_exception_compiled.argtypes = [ct.c_int]
lib.fma_exception_compiled.restype = ct.c_bool
