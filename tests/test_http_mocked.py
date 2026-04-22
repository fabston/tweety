"""HTTP-mocked unit tests using respx.

Demonstrates the intended pattern for testing request-path code without hitting
the live Twitter API. Extend this file with more mocked scenarios.
"""

import pytest

respx = pytest.importorskip("respx")


@pytest.mark.asyncio
async def test_respx_can_mock_httpx_get():
    """Sanity check that respx is wired up and can intercept httpx."""
    import httpx

    with respx.mock(assert_all_called=True) as router:
        router.get("https://example.test/ping").respond(200, json={"ok": True})
        async with httpx.AsyncClient() as client:
            r = await client.get("https://example.test/ping")
        assert r.status_code == 200
        assert r.json() == {"ok": True}


@pytest.mark.asyncio
async def test_respx_intercepts_post_with_body():
    import httpx

    with respx.mock as router:
        route = router.post("https://example.test/echo").respond(
            200, json={"received": True}
        )
        async with httpx.AsyncClient() as client:
            r = await client.post("https://example.test/echo", json={"a": 1})
        assert r.status_code == 200
        assert route.called
        import json as _json
        assert _json.loads(route.calls.last.request.read()) == {"a": 1}
