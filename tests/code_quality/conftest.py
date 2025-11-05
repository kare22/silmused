"""
Pytest configuration for code quality tests.
"""
import pytest


@pytest.fixture(scope="session")
def project_root():
    """Return the project root directory."""
    import os
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

