from datetime import datetime

import pytest

from skill_ci_status.dashboard import Card, Package, Job, Build, Branch, cards_to_json
from skill_ci_status.web import get_dashboard


@pytest.mark.asyncio
async def test_dashboard_json():
    print(await get_dashboard(None))

