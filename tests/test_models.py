"""Test the models."""

from __future__ import annotations

from typing import TYPE_CHECKING

from aresponses import ResponsesMockServer
from syrupy.assertion import SnapshotAssertion

from . import load_fixtures

if TYPE_CHECKING:
    from zurich import DisabledParking, ODPZurich


async def test_disabled_parkings(
    aresponses: ResponsesMockServer,
    snapshot: SnapshotAssertion,
    odp_zurich_client: ODPZurich,
) -> None:
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
    spaces: list[DisabledParking] = await odp_zurich_client.disabled_parkings()
    assert spaces == snapshot
