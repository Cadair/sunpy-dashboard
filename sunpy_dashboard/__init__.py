"""
An opsdroid skill for ci status monitoring.
"""

__version__ = "0.0.1.dev"

from pathlib import Path
from functools import partial
from logging import getLogger

from aiohttp.web import FileResponse

from .api import _ROUTES


log = getLogger(__name__)


async def serve_dashboard_html(request):
    return FileResponse(Path(__file__).parent / "dashboard" / "index.html")


def setup(opsdroid, config):
    app = opsdroid.web_server.web_app

    app.router.add_get('/', serve_dashboard_html)
    app.router.add_get('/dashboard', serve_dashboard_html)

    for endpoint, func in _ROUTES:
        app.router.add_get(endpoint, partial(func, opsdroid))
