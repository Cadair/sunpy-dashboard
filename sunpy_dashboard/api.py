import json
from typing import Annotated

import aiohttp

from fastapi import Path, HTTPException

from pydantic.json import pydantic_encoder

from sunpy_dashboard.packages import (
    build_packages,
    get_package_by_name,
    get_latest_build_for_branch,
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
async def get_latest_build(package: Annotated[str, Path(title="package name")],
                           branch: Annotated[str, Path(title="branch name")]):
    async with aiohttp.ClientSession() as session:
        package = await get_package_by_name(session, package)
        if branch not in package.active_branches:
            raise HTTPException(
                status_code=404,
                detail=f"branch {branch} is not in {package.name}'s configured active branches",
            )
        return await get_latest_build_for_branch(session, branch, package)
