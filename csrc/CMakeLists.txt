cmake_minimum_required(VERSION 3.25)

set(CMAKE_C_STANDARD 11)
set(CMAKE_C_STANDARD_REQUIRED ON)

# ---------------------------------------------------------------------------
# Feature detection: try_compile each <fenv.h> capability from an independent
# .c source file.  Each test verifies that the macro is defined.
# ---------------------------------------------------------------------------

set(_try_dir "${PROJECT_SOURCE_DIR}/cmake/try_compile")

try_compile(HAVE_FE_DIVBYZERO "${CMAKE_CURRENT_BINARY_DIR}/try_fe_divbyzero"
  SOURCES "${_try_dir}/check_fe_divbyzero.c"
  C_STANDARD 11
  C_STANDARD_REQUIRED YES
)

try_compile(HAVE_FE_INEXACT "${CMAKE_CURRENT_BINARY_DIR}/try_fe_inexact"
  SOURCES "${_try_dir}/check_fe_inexact.c"
  C_STANDARD 11
  C_STANDARD_REQUIRED YES
)

try_compile(HAVE_FE_INVALID "${CMAKE_CURRENT_BINARY_DIR}/try_fe_invalid"
  SOURCES "${_try_dir}/check_fe_invalid.c"
  C_STANDARD 11
  C_STANDARD_REQUIRED YES
)

try_compile(HAVE_FE_OVERFLOW "${CMAKE_CURRENT_BINARY_DIR}/try_fe_overflow"
  SOURCES "${_try_dir}/check_fe_overflow.c"
  C_STANDARD 11
  C_STANDARD_REQUIRED YES
)

try_compile(HAVE_FE_UNDERFLOW "${CMAKE_CURRENT_BINARY_DIR}/try_fe_underflow"
  SOURCES "${_try_dir}/check_fe_underflow.c"
  C_STANDARD 11
  C_STANDARD_REQUIRED YES
)

try_compile(HAVE_FE_TONEAREST "${CMAKE_CURRENT_BINARY_DIR}/try_fe_tonearest"
  SOURCES "${_try_dir}/check_fe_tonearest.c"
  C_STANDARD 11
  C_STANDARD_REQUIRED YES
)

try_compile(HAVE_FE_UPWARD "${CMAKE_CURRENT_BINARY_DIR}/try_fe_upward"
  SOURCES "${_try_dir}/check_fe_upward.c"
  C_STANDARD 11
  C_STANDARD_REQUIRED YES
)

try_compile(HAVE_FE_DOWNWARD "${CMAKE_CURRENT_BINARY_DIR}/try_fe_downward"
  SOURCES "${_try_dir}/check_fe_downward.c"
  C_STANDARD 11
  C_STANDARD_REQUIRED YES
)

try_compile(HAVE_FE_TOWARDZERO "${CMAKE_CURRENT_BINARY_DIR}/try_fe_towardzero"
  SOURCES "${_try_dir}/check_fe_towardzero.c"
  C_STANDARD 11
  C_STANDARD_REQUIRED YES
)

configure_file(
  "${PROJECT_SOURCE_DIR}/cmake/test_exception_round_support.h.in"
  "${CMAKE_CURRENT_BINARY_DIR}/fma_config.h"
)

add_library(fma_module SHARED fma_module.c)

target_sources(fma_module PUBLIC
  FILE_SET HEADERS
    BASE_DIRS "${CMAKE_CURRENT_SOURCE_DIR}"
    FILES fma_module.h
)

if(NOT WIN32)
  target_link_libraries(fma_module PRIVATE m)
endif()
target_include_directories(fma_module PRIVATE "${CMAKE_CURRENT_BINARY_DIR}")

if(MSVC)
  target_compile_options(fma_module PRIVATE /fp:strict)
elseif(CMAKE_C_COMPILER_ID MATCHES "Clang" OR CMAKE_C_COMPILER_ID MATCHES "GNU")
  target_compile_options(fma_module PRIVATE -frounding-math -fsignaling-nans)
endif()

install(
  TARGETS fma_module
  LIBRARY DESTINATION "python_fma"
)
