"""
An opsdroid skill for ci status monitoring.
"""

__version__ = "0.0.1.dev"

from pathlib import Path
from functools import partial
from logging import getLogger

from aiohttp.web import FileResponse, Response

from .dashboard import get_dashboard

from opsdroid.skill import Skill
from opsdroid.matchers import match_event
from opsdroid.events import OpsdroidStarted

log = getLogger(__name__)


async def serve_dashboard_html(request):
    return FileResponse(Path(__file__).parent / "dashboard" / "index.html")


async def serve_api_dashboard(opsdroid, request):
    return Response(body=await get_dashboard(opsdroid),
                    headers={"Access-Control-Allow-Origin": "*"})


def setup(opsdroid, config):
    app = opsdroid.web_server.web_app

    app.router.add_get('/dashboard', serve_dashboard_html)
    app.router.add_get('/api/dashboard', partial(serve_api_dashboard, opsdroid))
