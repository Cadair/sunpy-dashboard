import json
from typing import List
from pathlib import Path
from functools import cache

from .base import Package, get_pypi_version_time, Build, Branch, Card
from .providers import supported_providers


async def get_latest_builds(session, package):
    """
    Get all the latest builds for all active_branches for each service in ci_info.
    """
    branches = {}
    for branch in package.active_branches:
        branches[branch] = await get_latest_build_for_branch(session, branch, package)
    return branches


async def get_latest_build_for_branch(session, branch, package):
        builds = []
        for ci_name, config in package._ci_config.items():
            provider = supported_providers[ci_name](session)
            config.update({"branch": branch})
            last_build = await provider.get_last_build(**config)
            if last_build:
                builds.append(last_build)

        status_ordered = ['out-of-date', 'failed', 'succeeded', 'running', 'unknown']
        prioritized_status = [status_ordered.index(b.status) for b in builds]
        aggregate_status = status_ordered[min(prioritized_status)] if prioritized_status else "unknown"
        return Branch(aggregate_status, builds)


@cache
def get_packages_config():
    """
    Read the packages.json file.
    """
    with open(Path(__file__).parent / "dashboard" / "packages.json") as fobj:
        return json.loads(fobj.read())


async def get_package_by_name(session, package_name: str) -> Package:
    """
    Get a package instance for a name of a configured package.
    """
    packages = get_packages_config()
    pconfig = packages[package_name]
    version, last_release = await get_pypi_version_time(session,
                                                        pconfig["pypi_name"])
    package = Package(
                name=package_name,
                version=version,
                last_release=last_release,
                repourl=f"https://github.com/{pconfig['repo']}",
                logo=pconfig.get("logo", None),
                active_branches=pconfig["active_branches"],
    )
    package._ci_config = pconfig["ci"]
    return package


async def build_packages(session, config) -> List[Package]:
    """
    Build `Package` classes for all repos in config.
    """
    packages = []
    for package, pconfig in config.items():
        version, last_release = await get_pypi_version_time(session,
                                                            pconfig["pypi_name"])
        packages.append(await get_package_by_name(session, package))
    return packages


async def build_cards(session, packages: List[Package]) -> List[Card]:
    """
    Get all cards for all packages in the config.
    """
    cards = []
    for package in packages:
        cards.append(
            Card(
                package,
                await get_latest_builds(session, package)
                )
            )
    return cards
