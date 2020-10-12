"""
Base types for representing data.
"""
from datetime import datetime
from typing import List, Optional, Literal, Dict

from pydantic import HttpUrl
from pydantic.dataclasses import dataclass


async def get_pypi_version_time(session, name):
    """
    Get the last release and it's date from pypi.
    """
    url = f"https://pypi.org/pypi/{name}/json"

    async with session.get(url) as resp:
        info = (await resp.json())
    version = info["info"]["version"]
    time = datetime.fromisoformat(info["releases"][version][0]["upload_time"])
    return version, time


@dataclass
class Package():
    """
    Metadata about a package.
    """
    name: str
    version: str
    last_release: datetime
    active_branches: List[str]
    logo: Optional[HttpUrl] = None


@dataclass
class Job():
    """
    Information about a single CI job.
    """
    name: str
    status: Literal["succeeded", "failed", "skipped"]


@dataclass
class Build():
    """
    A single CI run.
    """
    service_name: str
    url: HttpUrl
    status: Literal["succeeded", "failed", "out-of-date"]
    time: datetime
    jobs: List[Job]


@dataclass
class Branch():
    status: Literal["succeeded", "failed", "out-of-date", "unknown"]
    builds: List[Build]


@dataclass
class Card():
    package: Package
    branches: Dict[str, Branch]
