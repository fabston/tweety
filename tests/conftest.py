"""Shared pytest fixtures for tweety tests."""

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

# Legacy standalone scripts — kept for reference but not collected by pytest.
# They run against the live API and are superseded by test_integration.py.
collect_ignore = [
    "test_basic.py",
    "test_authenticated.py",
    "test_comprehensive.py",
    "test_profile_images.py",
    "demo.py",
]


@pytest.fixture
def twitter_sync():
    from tweety import Twitter

    return Twitter("pytest-session")


@pytest.fixture
def twitter_async():
    from tweety import TwitterAsync

    return TwitterAsync("pytest-session-async")
