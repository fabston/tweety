"""Fast smoke tests — no network, no credentials."""

import pytest


def test_package_importable():
    import tweety

    assert hasattr(tweety, "Twitter")
    assert hasattr(tweety, "TwitterAsync")


def test_sync_client_initializes(twitter_sync):
    assert twitter_sync.session.session_name == "pytest-session"
    assert twitter_sync.logged_in is False
    assert twitter_sync.is_user_authorized is False


def test_async_client_initializes(twitter_async):
    assert twitter_async.session.session_name == "pytest-session-async"
    assert twitter_async.logged_in is False


def test_sync_client_properties(twitter_sync):
    assert twitter_sync.user_id is None
    assert twitter_sync.cache == {}


def test_exceptions_module_reexport():
    from tweety.exceptions import TwitterError as E1
    from tweety.exceptions_ import TwitterError as E2

    assert E1 is E2


def test_models_reexport_is_same_class():
    from tweety.models.tweet import Tweet as T1
    from tweety.types.twDataTypes import Tweet as T2

    assert T1 is T2


def test_models_media_reexports():
    from tweety.models.media import Media, Stream
    from tweety.types.twDataTypes import Media as M2
    from tweety.types.twDataTypes import Stream as S2

    assert Media is M2
    assert Stream is S2


class TestMediaResPixels:
    """Regression tests for the eval() -> safe parse fix in Media.best_stream."""

    def _media_cls(self):
        from tweety.types.twDataTypes import Media

        return Media

    def test_resolution_parses_correctly(self):
        assert self._media_cls()._res_pixels("1920*1080") == 2073600
        assert self._media_cls()._res_pixels("640*480") == 307200

    def test_resolution_none_is_zero(self):
        assert self._media_cls()._res_pixels(None) == 0

    def test_resolution_empty_is_zero(self):
        assert self._media_cls()._res_pixels("") == 0

    def test_resolution_malformed_is_zero(self):
        # Previous eval() would have raised; now we return 0 safely.
        assert self._media_cls()._res_pixels("not-a-resolution") == 0
        assert self._media_cls()._res_pixels("__import__('os').system('echo x')") == 0


def test_utils_find_objects():
    from tweety.utils import find_objects

    data = {"a": {"b": 1, "c": {"b": 2}}}
    assert find_objects(data, "b", None) == [1, 2]
    assert find_objects(data, "missing", None, none_value="default") == "default"


def test_utils_parse_time_datetime_passthrough():
    import datetime

    from tweety.utils import parse_time

    dt = datetime.datetime(2024, 1, 2, 3, 4, 5)
    assert parse_time(dt) is dt


def test_utils_parse_wait_time_scalars():
    from tweety.utils import parse_wait_time

    assert parse_wait_time(None) == 0
    assert parse_wait_time(5) == 5
    assert parse_wait_time("3") == 3


def test_utils_parse_wait_time_tuple_is_in_range():
    from tweety.utils import parse_wait_time

    for _ in range(20):
        assert 1 <= parse_wait_time((1, 3)) <= 3


def test_utils_create_conversation_id_canonical_order():
    from tweety.utils import create_conversation_id

    assert create_conversation_id(7, 3) == "3-7"
    assert create_conversation_id(3, 7) == "3-7"


def test_utils_get_tweet_id_from_url():
    from tweety.utils import get_tweet_id

    url = "https://twitter.com/elonmusk/status/1234567890"
    assert get_tweet_id(url) == "1234567890"


@pytest.mark.parametrize(
    "res,expected",
    [
        ("100*100", 10000),
        ("1*1", 1),
        ("0*0", 0),
        (None, 0),
    ],
)
def test_media_res_pixels_parametrized(res, expected):
    from tweety.types.twDataTypes import Media

    assert Media._res_pixels(res) == expected
