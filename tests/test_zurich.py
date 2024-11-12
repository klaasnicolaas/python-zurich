"""Basic tests for the Open Data Platform API of Zurich."""

# pylint: disable=protected-access
import asyncio
from unittest.mock import patch

import pytest
from aiohttp import ClientError, ClientResponse, ClientSession
from aresponses import Response, ResponsesMockServer

from zurich import ODPZurich
from zurich.exceptions import ODPZurichConnectionError, ODPZurichError

from . import load_fixtures


async def test_json_request(
    aresponses: ResponsesMockServer, odp_zurich_client: ODPZurich
) -> None:
    """Test JSON response is handled correctly."""
    aresponses.add(
        "www.ogd.stadt-zuerich.ch",
        "/wfs/geoportal/test",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/vnd.geo+json"},
            text=load_fixtures("disabled_parkings.json"),
        ),
    )
    await odp_zurich_client._request("test")
    await odp_zurich_client.close()


async def test_internal_session(aresponses: ResponsesMockServer) -> None:
    """Test internal session is handled correctly."""
    aresponses.add(
        "www.ogd.stadt-zuerich.ch",
        "/wfs/geoportal/test",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/vnd.geo+json"},
            text=load_fixtures("disabled_parkings.json"),
        ),
    )
    async with ODPZurich() as client:
        await client._request("test")


async def test_timeout(aresponses: ResponsesMockServer) -> None:
    """Test request timeout from the Open Data Platform API of Zurich."""

    # Faking a timeout by sleeping
    async def response_handler(_: ClientResponse) -> Response:
        await asyncio.sleep(0.2)
        return aresponses.Response(
            body="Goodmorning!",
            text=load_fixtures("disabled_parkings.json"),
        )

    aresponses.add(
        "www.ogd.stadt-zuerich.ch",
        "/wfs/geoportal/test",
        "GET",
        response_handler,
    )

    async with ClientSession() as session:
        client = ODPZurich(
            session=session,
            request_timeout=0.1,
        )
        with pytest.raises(ODPZurichConnectionError):
            assert await client._request("test")


async def test_content_type(
    aresponses: ResponsesMockServer, odp_zurich_client: ODPZurich
) -> None:
    """Test request content type error from Open Data Platform API of Zurich."""
    aresponses.add(
        "www.ogd.stadt-zuerich.ch",
        "/wfs/geoportal/test",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "blabla/blabla"},
        ),
    )
    with pytest.raises(ODPZurichError):
        assert await odp_zurich_client._request("test")


async def test_client_error() -> None:
    """Test request client error from the Open Data Platform API of Zurich."""
    async with ClientSession() as session:
        client = ODPZurich(session=session)
        with (
            patch.object(
                session,
                "request",
                side_effect=ClientError,
            ),
            pytest.raises(ODPZurichConnectionError),
        ):
            assert await client._request("test")
