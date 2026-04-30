#pragma once

// Floating-point exception support (from <fenv.h>)
#define HAVE_FE_DIVBYZERO 1
#define HAVE_FE_INEXACT 1
#define HAVE_FE_INVALID 1
#define HAVE_FE_OVERFLOW 1
#define HAVE_FE_UNDERFLOW 1

// Rounding mode support (from <fenv.h>)
#define HAVE_FE_TONEAREST 1
#define HAVE_FE_UPWARD 1
#define HAVE_FE_DOWNWARD 1
#define HAVE_FE_TOWARDZERO 1
