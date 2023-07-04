# pylint: disable=W0621
"""Asynchronous Python client providing Open Data information of Zurich."""

import asyncio

from zurich import ODPZurich


async def main() -> None:
    """Show example on using the Zurich API client."""
    async with ODPZurich() as client:
        disabled_parkings = await client.disabled_parkings()

        count: int = len(disabled_parkings)
        for item in disabled_parkings:
            print(item)

        # Count unique id's in disabled_parkings
        unique_values: list[str] = [str(item.spot_id) for item in disabled_parkings]
        num_values = len(set(unique_values))

        print("__________________________")
        print(f"Total locations found: {count}")
        print(f"Unique ID values: {num_values}")


if __name__ == "__main__":
    asyncio.run(main())
