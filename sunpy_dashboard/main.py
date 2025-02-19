from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

__all__ = ['app']

app = FastAPI()

app.mount("/dashboard", StaticFiles(directory=Path(__file__).parent / "dashboard", html=True), name="dashboard")

import sunpy_dashboard.api  # noqa
