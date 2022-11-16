"""
Functions for interacting with the GitHub Actions API.
"""
import os
from typing import List
from logging import getLogger
from datetime import datetime, timedelta

from ..base import Job, Build
from .base import BaseProvider

log = getLogger(__name__)


def map_status(job):
    mapping = {
        "success": "succeeded",
        "failure": "failed",
        "cancelled": "failed",
        "timed_out": "failed",
    }

    return mapping.get(job["conclusion"], "unknown")


class GitHubProvider(BaseProvider):
    async def make_request(self, method: str,
                           endpoint: str,
                           *,
                           params=None,
                           data=None,
                           **kwargs):
        headers = {}
        if "GITHUB_PERSONAL_ACCESS_TOKEN" in os.environ:
            headers = {
                "Authorization": f"token {os.environ['GITHUB_PERSONAL_ACCESS_TOKEN']}"
            }
        return await super().make_request(method, endpoint, params=params, data=data, headers=headers)

    async def get_last_build_on_branch(
            self, org: str, project: str, branch: str, workflow_name: str
    ) -> dict:
        """
        Request the last build on a given branch, return the json.
        """
        endpoint = f"https://api.github.com/repos/{org}/{project}/actions/runs"
        params = {"branch": f"{branch}", "status": "completed"}

        builds = None
        try:
            builds = await self.make_request("GET", endpoint, params=params)
            builds = builds["workflow_runs"]
        except Exception:
            log.exception(f"Unable to fetch last pipelines build for {org}/{project}")
            log.error(builds)
            pass
        if builds:
            if workflow_name:
                for build in builds:
                    if build["name"] == workflow_name:
                        return build
                log.exception("Could not find a workflow named CI")
            return builds[0]

    async def get_workflow_jobs(self, jobs_url: str) -> List[Job]:
        """
        Parse the timeline and get the jobs (phases) and their statuses.
        """
        jobs = (await self.make_request("GET", jobs_url))["jobs"]
        # none is not allowed but is returned when a build is running
        return [Job(j["name"], map_status(j)) for j in jobs]

    async def get_last_build(self, org: str, repo: str, branch: str, workflow_name: str = None) -> Build:
        """
        Get a reduced report about the last job,
        including the status of the individual jobs.
        """
        resp = await self.get_last_build_on_branch(org, repo, branch, workflow_name)
        if resp:
            status = map_status(resp)
            status = status if status not in ("abandoned",) else "unknown"
            last_time = datetime.fromisoformat(resp["run_started_at"].split(":")[0])
            if datetime.now() - last_time > timedelta(hours=32):
                status = "out-of-date"
            return Build(
                id=resp["id"],
                service_name="GitHub Actions",
                url=resp["html_url"],
                status=status,
                time=last_time,
                jobs=await self.get_workflow_jobs(resp["jobs_url"]),
            )
