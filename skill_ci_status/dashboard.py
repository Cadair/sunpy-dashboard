"""
Data models relating to the dashboard
"""
import json
from datetime import datetime
from typing import Dict, List, Optional

from pydantic.dataclasses import dataclass
from pydantic.json import pydantic_encoder


@dataclass
class Package():
    name: str
    version: str
    logo: Optional[str] = None


@dataclass
class Job():
    name: str
    status: str


@dataclass
class Build():
    url: str
    status: str
    time: datetime
    jobs: List[Job]


@dataclass
class Branch():
    build: Build


@dataclass
class Card():
    package: Package
    branches: Dict[str, Branch]


def cards_to_json(cards):
    """
    Serialise a Card to json
    """
    return json.dumps(cards, indent=2, default=pydantic_encoder)
