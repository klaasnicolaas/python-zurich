"""Fixture for the ODP Zurich tests."""

from collections.abc import AsyncGenerator

import pytest
from aiohttp import ClientSession

from zurich import ODPZurich


@pytest.fixture(name="odp_zurich_client")
async def client() -> AsyncGenerator[ODPZurich, None]:
    """Return an ODP Zurich client."""
    async with (
        ClientSession() as session,
        ODPZurich(session=session) as odp_zurich_client,
    ):
        yield odp_zurich_client
