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
                           data=None,
                           **kwargs):
        """
        Make a request with aiohttp, return json content.
        """
        async with self.session.request(method,
                                        endpoint,
                                        params=params,
                                        data=data,
                                        **kwargs) as resp:
            return await resp.json()

    @abstractmethod
    async def get_last_build(self,
                             org: str,
                             repo: str,
                             branch: str) -> Build:
        """
        Generate a report about the last build
        """
