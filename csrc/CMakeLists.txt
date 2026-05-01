cmake_minimum_required(VERSION 3.25)

set(CMAKE_C_STANDARD 11)
set(CMAKE_C_STANDARD_REQUIRED ON)

add_library(fma_module SHARED fma_module.c)

target_sources(fma_module PUBLIC
  FILE_SET HEADERS
    BASE_DIRS "${CMAKE_CURRENT_SOURCE_DIR}"
    FILES fma_module.h
)

if(NOT WIN32)
  target_link_libraries(fma_module PRIVATE m)
endif()

if(MSVC)
  target_compile_options(fma_module PRIVATE /fp:strict)
elseif(CMAKE_C_COMPILER_ID MATCHES "Clang" OR CMAKE_C_COMPILER_ID MATCHES "GNU")
  target_compile_options(fma_module PRIVATE -frounding-math -fsignaling-nans)
endif()

install(
  TARGETS fma_module
  LIBRARY DESTINATION "python_fma"
)
