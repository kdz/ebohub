import pytest
from src import db_init


def test_db_rebuild():
    try:
        db_init.db_reset()
    except Exception:
        pytest.fail("DB rebuild failure")

