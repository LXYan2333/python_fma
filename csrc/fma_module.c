#include "fma_module.h"

#include <fenv.h>
#include <math.h>

#include "fma_config.h"

static int fe_round_from_fma_round(int round_mode) {
  switch (round_mode) {
  case FMA_TONEAREST:
#if HAVE_FE_TONEAREST
    return FE_TONEAREST;
#endif
    break;
  case FMA_UPWARD:
#if HAVE_FE_UPWARD
    return FE_UPWARD;
#endif
    break;
  case FMA_DOWNWARD:
#if HAVE_FE_DOWNWARD
    return FE_DOWNWARD;
#endif
    break;
  case FMA_TOWARDZERO:
#if HAVE_FE_TOWARDZERO
    return FE_TOWARDZERO;
#endif
    break;
  }
  return -1;
}

static void set_exc_flags(int fe_flags, bool *exc_invalid, bool *exc_divbyzero,
                          bool *exc_overflow, bool *exc_underflow,
                          bool *exc_inexact) {
#if HAVE_FE_INVALID
  *exc_invalid = (fe_flags & FE_INVALID) ? true : false;
#else
  *exc_invalid = false;
#endif
#if HAVE_FE_DIVBYZERO
  *exc_divbyzero = (fe_flags & FE_DIVBYZERO) ? true : false;
#else
  *exc_divbyzero = false;
#endif
#if HAVE_FE_OVERFLOW
  *exc_overflow = (fe_flags & FE_OVERFLOW) ? true : false;
#else
  *exc_overflow = false;
#endif
#if HAVE_FE_UNDERFLOW
  *exc_underflow = (fe_flags & FE_UNDERFLOW) ? true : false;
#else
  *exc_underflow = false;
#endif
#if HAVE_FE_INEXACT
  *exc_inexact = (fe_flags & FE_INEXACT) ? true : false;
#else
  *exc_inexact = false;
#endif
}

double fma_double(double x, double y, double z, int round_mode,
                  bool *exc_invalid, bool *exc_divbyzero, bool *exc_overflow,
                  bool *exc_underflow, bool *exc_inexact) {
  int old_round = 0;
  bool need_restore = false;

  if (round_mode != FMA_DYNAMIC) {
    old_round = fegetround();
    fesetround(fe_round_from_fma_round(round_mode));
    need_restore = true;
  }

  feclearexcept(FE_ALL_EXCEPT);
  double result = fma(x, y, z);
  set_exc_flags(fetestexcept(FE_ALL_EXCEPT), exc_invalid, exc_divbyzero,
                exc_overflow, exc_underflow, exc_inexact);

  if (need_restore) {
    fesetround(old_round);
  }
  return result;
}

float fma_float(float x, float y, float z, int round_mode, bool *exc_invalid,
                bool *exc_divbyzero, bool *exc_overflow, bool *exc_underflow,
                bool *exc_inexact) {
  int old_round = 0;
  bool need_restore = false;

  if (round_mode != FMA_DYNAMIC) {
    old_round = fegetround();
    fesetround(fe_round_from_fma_round(round_mode));
    need_restore = true;
  }

  feclearexcept(FE_ALL_EXCEPT);
  float result = fmaf(x, y, z);
  set_exc_flags(fetestexcept(FE_ALL_EXCEPT), exc_invalid, exc_divbyzero,
                exc_overflow, exc_underflow, exc_inexact);

  if (need_restore) {
    fesetround(old_round);
  }
  return result;
}

bool fma_round_mode_supported(int round_mode) {
  int fe_round = fe_round_from_fma_round(round_mode);
  if (fe_round < 0) {
    return false;
  }

  int old = fegetround();
  bool ok = (fesetround(fe_round) == 0);
  fesetround(old);
  return ok;
}

bool fma_round_mode_compiled(int round_mode) {
  switch (round_mode) {
  case FMA_TONEAREST:
    return HAVE_FE_TONEAREST;
  case FMA_UPWARD:
    return HAVE_FE_UPWARD;
  case FMA_DOWNWARD:
    return HAVE_FE_DOWNWARD;
  case FMA_TOWARDZERO:
    return HAVE_FE_TOWARDZERO;
  default:
    return false;
  }
}

bool fma_exception_compiled(enum fma_exc_type exc) {
  switch (exc) {
  case FMA_EXC_INVALID:
    return HAVE_FE_INVALID;
  case FMA_EXC_DIVBYZERO:
    return HAVE_FE_DIVBYZERO;
  case FMA_EXC_OVERFLOW:
    return HAVE_FE_OVERFLOW;
  case FMA_EXC_UNDERFLOW:
    return HAVE_FE_UNDERFLOW;
  case FMA_EXC_INEXACT:
    return HAVE_FE_INEXACT;
  default:
    return 0;
  }
}
