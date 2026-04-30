#pragma once

#include <stdbool.h>

enum fma_round_mode {
  FMA_TONEAREST = 0,
  FMA_UPWARD = 1,
  FMA_DOWNWARD = 2,
  FMA_TOWARDZERO = 3,
  FMA_DYNAMIC = -1,
};

enum fma_exc_type {
  FMA_EXC_INVALID,
  FMA_EXC_DIVBYZERO,
  FMA_EXC_OVERFLOW,
  FMA_EXC_UNDERFLOW,
  FMA_EXC_INEXACT,
};

double fma_double(double x, double y, double z, int round_mode,
                  bool *exc_invalid, bool *exc_divbyzero, bool *exc_overflow,
                  bool *exc_underflow, bool *exc_inexact);

float fma_float(float x, float y, float z, int round_mode, bool *exc_invalid,
                bool *exc_divbyzero, bool *exc_overflow, bool *exc_underflow,
                bool *exc_inexact);

bool fma_round_mode_supported(int round_mode);

bool fma_round_mode_compiled(int round_mode);

bool fma_exception_compiled(enum fma_exc_type exc);
