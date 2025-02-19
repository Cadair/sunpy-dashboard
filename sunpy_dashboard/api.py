import json

import aiohttp

from pydantic.json import pydantic_encoder

from sunpy_dashboard.packages import (
    build_packages,
    #get_latest_build_for_branch,
    get_packages_config,
    build_cards,
)

from sunpy_dashboard.main import app


def to_json(data):
    """
    Serialise a Card to json
    """
    return json.dumps(data, indent=2, default=pydantic_encoder)


@app.get("/api/dashboard")
async def serve_api_dashboard():
    """
    Returns the whole filled up dashboard JSON.
    """
    async with aiohttp.ClientSession() as session:
        return await build_cards(
            session, await build_packages(session, get_packages_config())
        )


@app.get("/api/packages")
async def get_packages():
    async with aiohttp.ClientSession() as session:
        return await build_packages(session, get_packages_config())


@app.get("/api/latest_build/{package}/{branch}")
async def get_latest_build(request):
    pass


@app.get("/api/jobs/{package}/{branch}/{job_id}")
async def get_jobs(request):
    pass
