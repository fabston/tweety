"""Integration tests that hit the live Twitter API.

These auto-enable if a session file is present next to this file
(``test_session_1.tw_session``). Otherwise they skip. Can also be forced on
with ``TWEETY_LIVE=1`` — in which case a ``test_session_1`` session file is
still expected.
"""

import os
from pathlib import Path

import pytest

SESSION_DIR = Path(__file__).parent
SESSION_NAME = "test_session_1"
SESSION_FILE = SESSION_DIR / f"{SESSION_NAME}.tw_session"

pytestmark = pytest.mark.skipif(
    not SESSION_FILE.exists() and os.environ.get("TWEETY_LIVE") != "1",
    reason=f"No session file at {SESSION_FILE}; set TWEETY_LIVE=1 or drop a .tw_session there",
)


@pytest.fixture
def live_app():
    from tweety import TwitterAsync

    return TwitterAsync(str(SESSION_DIR / SESSION_NAME))


@pytest.mark.asyncio
async def test_connect_loads_session(live_app):
    user = await live_app.connect()
    assert user is not None
    assert live_app.is_user_authorized is True
    assert user.id is not None


@pytest.mark.asyncio
async def test_public_user_info_elonmusk(live_app):
    await live_app.connect()
    user = await live_app.get_user_info("elonmusk")
    assert user is not None
    assert str(user.username).lower() == "elonmusk"
    assert user.id is not None


@pytest.mark.asyncio
async def test_public_tweets_first_page(live_app):
    await live_app.connect()
    tweets = await live_app.get_tweets("elonmusk", pages=1)
    assert tweets is not None
    assert len(tweets) > 0
    assert tweets[0].id is not None


@pytest.mark.skipif(
    os.environ.get("TWEETY_LIVE_WRITE") != "1",
    reason="Set TWEETY_LIVE_WRITE=1 to run write-tests (posts then deletes a tweet)",
)
@pytest.mark.asyncio
async def test_create_and_delete_tweet(live_app):
    """Posts a uniquely-marked tweet, verifies it, then deletes it.

    If deletion fails, the test fails and the tweet is findable by its marker.
    """
    import time

    await live_app.connect()
    marker = f"tweety-integration-test {int(time.time())}"
    text = f"{marker} — automated test, deleting immediately. Please ignore."

    posted = await live_app.create_tweet(text=text)
    assert posted is not None
    assert posted.id is not None
    assert marker in posted.text

    try:
        deleted = await live_app.delete_tweet(posted.id)
        assert deleted is True, f"Failed to delete tweet {posted.id}"
    except Exception:
        pytest.fail(
            f"Posted tweet {posted.id} with marker '{marker}' — deletion failed, "
            f"please delete it manually."
        )
