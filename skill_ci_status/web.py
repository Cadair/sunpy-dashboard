import json
from pathlib import Path

import aiohttp

from .base import Package, get_pypi_version_time
from .dashboard import Branch, Card, cards_to_json
from .providers import supported_providers


async def get_latest_builds(session, active_branches, ci_info):
    branches = {}
    for branch in active_branches:
        builds = []
        for ci_name, config in ci_info.items():
            provider = supported_providers[ci_name](session)
            last_build = await provider.get_last_build(config['org'],
                                                       config['repo'],
                                                       branch)
            if last_build:
                builds.append(last_build)

        aggregate_status = "failed" if "failed" in [b.status for b in builds] else "succeeded"
        branches[branch] = Branch(aggregate_status, builds)
    return branches


async def build_cards(session):
    with open(Path(__file__).parent / "dashboard" / "packages.json") as fobj:
        packages = json.loads(fobj.read())

    cards = []
    for package, config in packages.items():
        version, last_release = await get_pypi_version_time(session, config["pypi_name"])
        cards.append(Card(
            Package(
                name=package,
                version=version,
                last_release=last_release,
                logo=config.get("logo", ""),
            ),
            await get_latest_builds(session, config["active_branches"], config["ci"])
        )
    )
    return cards


async def get_dashboard(opsdroid):
    """
    Get the data for the dashboard API response.
    """
    async with aiohttp.ClientSession() as session:
        return cards_to_json(await build_cards(session))
