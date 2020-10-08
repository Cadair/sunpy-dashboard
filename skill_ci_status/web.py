from datetime import datetime

from .dashboard import Card, Package, Job, Build, Branch, cards_to_json


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


async def get_dashboard(opsdroid):
    """
    Get the data for the dashboard api response.
    """
    return cards_to_json(example_cards)
