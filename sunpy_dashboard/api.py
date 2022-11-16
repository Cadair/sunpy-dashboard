import json

import aiohttp
from aiohttp.web import FileResponse, Response
from pydantic.json import pydantic_encoder

from sunpy_dashboard.packages import (
    build_packages,
    build_packages,
    get_latest_build_for_branch,
    get_packages_config,
    build_cards,
)

_ROUTES = []


def to_json(data):
    """
    Serialise a Card to json
    """
    return json.dumps(data, indent=2, default=pydantic_encoder)


def api_route(endpoint):
    def decorator(func):
        async def inner(*args, **kwargs):
            body = await func(*args, **kwargs)
            return Response(
                body=to_json(body), headers={"Access-Control-Allow-Origin": "*"}
            )

        _ROUTES.append((endpoint, inner))
        return inner

    return decorator


@api_route("/api/dashboard")
async def serve_api_dashboard(opsdroid, request):
    """
    Returns the whole filled up dashboard JSON.
    """
    async with aiohttp.ClientSession() as session:
        return await build_cards(
            session, await build_packages(session, get_packages_config())
        )


@api_route("/api/packages")
async def get_packages(opsdroid, request):
    async with aiohttp.ClientSession() as session:
        return await build_packages(session, get_packages_config())


@api_route("/api/latest_build/{package}/{branch}")
async def get_latest_build(opsdroid, request):
    pass


@api_route("/api/jobs/{package}/{branch}/{job_id}")
async def get_jobs(opsdroid, request):
    pass
