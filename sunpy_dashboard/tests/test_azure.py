import aiohttp
import pytest

from sunpy_dashboard.providers.base import JobReport, BuildReport
from sunpy_dashboard.providers.azure_pipelines import AzureProvider


@pytest.mark.asyncio
async def test_azure_get():
    async with aiohttp.ClientSession() as session:
        ap = AzureProvider(session)
        response = await ap.get_last_build_report("sunpy",
                                                  "sunpy",
                                                  "master")
        assert isinstance(response, BuildReport)
