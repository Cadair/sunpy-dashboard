import json
from typing import List
from pathlib import Path

from .base import Package, get_pypi_version_time, Build, Branch, Card
from .providers import supported_providers


async def get_latest_builds(session, active_branches, ci_info):
    """
    Get all the latest builds for all active_branches for each service in ci_info.
    """
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

        status_ordered = ['out-of-date', 'failed', 'succeeded', 'running', 'unknown']
        prioritized_status = [status_ordered.index(b.status) for b in builds]
        aggregate_status = status_ordered[min(prioritized_status)] if prioritized_status else "unknown"
        branches[branch] = Branch(aggregate_status, builds)
    return branches


def get_packages_config():
    """
    Read the packages.json file.
    """
    with open(Path(__file__).parent / "dashboard" / "packages.json") as fobj:
        return json.loads(fobj.read())


async def build_packages(session, config) -> List[Package]:
    """
    Build `Package` classes for all repos in config.
    """
    packages = []
    for package, pconfig in config.items():
        version, last_release = await get_pypi_version_time(session,
                                                            pconfig["pypi_name"])
        packages.append(
            Package(
                name=package,
                version=version,
                last_release=last_release,
                repourl=f"https://github.com/{pconfig['repo']}",
                logo=pconfig.get("logo", None),
                active_branches=pconfig["active_branches"],
            )
        )
        packages[-1]._ci_config = pconfig["ci"]
    return packages


async def get_builds_for_packages(session, package: Package) -> List[Build]:
    """
    Get latest builds for given package.
    """
    return await get_latest_builds(session,
                                   package.active_branches,
                                   package._ci_config)


async def build_cards(session, packages: List[Package]) -> List[Card]:
    """
    Get all cards for all packages in the config.
    """
    cards = []
    for package in packages:
        cards.append(
            Card(
                package,
                await get_builds_for_packages(session, package)
                )
            )
    return cards
