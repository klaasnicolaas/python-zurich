"""Test the models."""
from __future__ import annotations

from aiohttp import ClientSession
from aresponses import ResponsesMockServer

from zurich import DisabledParking, ODPZurich

from . import load_fixtures


async def test_disabled_parkings(aresponses: ResponsesMockServer) -> None:
    """Test disabled parking spaces function."""
    aresponses.add(
        "www.ogd.stadt-zuerich.ch",
        "/wfs/geoportal/Behindertenparkplaetze",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/vnd.geo+json"},
            text=load_fixtures("disabled_parkings.json"),
        ),
    )
    async with ClientSession() as session:
        client = ODPZurich(session=session)
        spaces: list[DisabledParking] = await client.disabled_parkings()
        assert spaces is not None
        for item in spaces:
            assert item.spot_id is not None
            assert item.longitude is not None
            assert item.latitude is not None
            assert isinstance(item.longitude, float)
            assert isinstance(item.latitude, float)
