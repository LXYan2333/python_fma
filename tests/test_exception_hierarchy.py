from python_fma import (
    DivByZeroException,
    FeatureNotCompiledError,
    FloatException,
    InexactException,
    InvalidException,
    OverflowException,
    UnderflowException,
    UnsupportedRoundingModeError,
)


class TestExceptionHierarchy:
    def test_float_exception_base(self):
        assert issubclass(InvalidException, FloatException)
        assert issubclass(DivByZeroException, FloatException)
        assert issubclass(OverflowException, FloatException)
        assert issubclass(UnderflowException, FloatException)
        assert issubclass(InexactException, FloatException)

    def test_feature_not_compiled_is_float_exception(self):
        assert issubclass(FeatureNotCompiledError, FloatException)

    def test_unsupported_rounding_mode_is_float_exception_and_value_error(self):
        assert issubclass(UnsupportedRoundingModeError, FloatException)
        assert issubclass(UnsupportedRoundingModeError, ValueError)
