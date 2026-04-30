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
# fmt: on")

_lib_name = f"libfma_module{_ext}"

# Editable installs (scikit-build-core) put the .so in site-packages while
# Python sources are imported from the source tree.  Use the import-system
# location first (via the editable hook's known_wheel_files mapping), then
# fall back to __file__-relative for regular installs.
_spec = _iu.find_spec(f"python_fma.{_lib_name.rsplit('.', 1)[0]}")
# fmt: off
if _spec is not None and _spec.origin is not None and os.path.exists(_spec.origin):
    _lib_path = _spec.origin
else:                                   # pragma: no cover
    _lib_path = os.path.join(os.path.dirname(__file__), _lib_name)
# fmt: on

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
