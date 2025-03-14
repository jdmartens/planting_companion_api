from unittest.mock import MagicMock, patch

from sqlmodel import select
from sqlalchemy.engine import Engine  # Add import for spec
from app.tests_pre_start import init, logger


def test_init_successful_connection() -> None:
    engine_mock = MagicMock(spec=Engine)

    session_mock = MagicMock()
    session_mock.__enter__.return_value = session_mock  # Context manager support
    exec_mock = MagicMock()
    session_mock.configure_mock(**{"exec.return_value": exec_mock})

    with (
        patch("app.tests_pre_start.Session", return_value=session_mock),
        patch.object(logger, "info"),
        patch.object(logger, "error"),
        patch.object(logger, "warn"),
    ):
        init(engine_mock)
        
        # 1. Verify exec was called once
        session_mock.exec.assert_called_once()  # Check call count
        
        # 2. Compare SQL content instead of object identity
        actual_stmt = session_mock.exec.call_args[0][0]
        expected_stmt = select(1)
        
        # Compare compiled SQL statements
        assert str(actual_stmt.compile(compile_kwargs={"literal_binds": True})) == \
               str(expected_stmt.compile(compile_kwargs={"literal_binds": True}))

