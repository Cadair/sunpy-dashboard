"""
Data models relating to the dashboard.
"""
import json
from typing import Dict, List, Literal

import aiohttp
from pydantic.dataclasses import dataclass
from pydantic.json import pydantic_encoder

from .base import Build, Package
from .packages import build_cards, build_packages, get_packages_config


def cards_to_json(cards):
    """
    Serialise a Card to json
    """
    return json.dumps(cards, indent=2, default=pydantic_encoder)


async def get_dashboard(opsdroid):
    """
    Get the data for the dashboard API response.
    """
    async with aiohttp.ClientSession() as session:
        return cards_to_json(
            await build_cards(session,
                              await build_packages(session,
                                                   get_packages_config()
                                                   )
                              )
        )
