from datetime import datetime

import pytest

from skill_ci_status.dashboard import Card, Package, Job, Build, Branch, cards_to_json
from skill_ci_status.web import get_dashboard

example_cards = [
    Card(
        Package(
            name="sunpy",
            version="v2.0.3",
            logo="https://raw.githubusercontent.com/sunpy/sunpy.org/master/_static/img/sunpy_icon.svg"
            ),
        {
            'master': Branch(
                Build(
                    url="https://bbc.co.uk",
                    status="success",
                    time=datetime(2011, 1, 1, 14, 5, 8),
                    jobs=[
                        Job(
                            "py38",
                            "faliure"
                        )
                    ]
                )
            ),
            '2.0': Branch(
                Build(
                    url="https://bbc.co.uk",
                    status="success",
                    time=datetime(2011, 1, 1, 14, 5, 8),
                    jobs=[
                        Job(
                            "py38",
                            "success"
                        )
                    ]
                )
            )
        }
    )
]

@pytest.mark.asyncio
async def test_dashboard_json():
    print(await get_dashboard(None))

