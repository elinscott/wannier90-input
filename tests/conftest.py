"""Test configuration."""

from pathlib import Path

import pytest


@pytest.fixture
def data_directory() -> Path:
    """Return the directory where we store data required for the test suite."""
    return Path(__file__).parent / 'data'
