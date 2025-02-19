A CI status dashboard for sunpy
================================

This repo uses fastapi to generate a simple dashboard showing the CI status for all the sunpy repos.

To run it you will almost certainly need to set the `GITHUB_PERSONAL_ACCESS_TOKEN` variable, then do `fastapi dev sunpy_dashboard/main.py`.
