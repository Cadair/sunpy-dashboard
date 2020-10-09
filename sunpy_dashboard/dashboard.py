"""
Data models relating to the dashboard.
"""
import json
from typing import Dict, List, Literal

from pydantic.dataclasses import dataclass
from pydantic.json import pydantic_encoder

from .base import Build, Package


@dataclass
class Branch():
    status: Literal["succeeded", "failed", "out-of-date", "unknown"]
    builds: List[Build]


@dataclass
class Card():
    package: Package
    branches: Dict[str, Branch]


def cards_to_json(cards):
    """
    Serialise a Card to json
    """
    return json.dumps(cards, indent=2, default=pydantic_encoder)
