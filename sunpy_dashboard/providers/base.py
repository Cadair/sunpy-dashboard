from abc import ABC, abstractmethod
from typing import List

from pydantic.dataclasses import dataclass

from ..base import Job, Build


class BaseProvider(ABC):
    """
    A representation of a CI provider.
    """

    def __init__(self, session):
        self.session = session

    async def make_request(self, method: str,
                           endpoint: str,
                           *,
                           params=None,
                           data=None):
        """
        Make a request with aiohttp, return json content.
        """
        async with self.session.request(method,
                                        endpoint,
                                        params=params,
                                        data=data) as resp:
            return await resp.json()

    @abstractmethod
    async def get_last_build(self,
                             org: str,
                             repo: str,
                             branch: str) -> Build:
        """
        Generate a report about the last build
        """

    @abstractmethod
    async def get_last_build_on_branch(self,
                                       org: str,
                                       repo: str,
                                       branch: str) -> dict:
        """
        Get the full json of the last build on the given branch.
        """
