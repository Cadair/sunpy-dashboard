"""
Functions for interacting with the Azure Pipelines API.
"""
from typing import List
from logging import getLogger
from datetime import datetime, timedelta

from ..base import Job, Build
from .base import BaseProvider

log = getLogger(__name__)


class AzureProvider(BaseProvider):

    async def get_last_build_on_branch(self,
                                       org: str,
                                       project: str,
                                       branch: str) -> dict:
        """
        Request the last build on a given branch, return the json.
        """
        endpoint = f"https://dev.azure.com/{org}/{project}/_apis/build/builds"
        params = {"api-version": 6,
                  "branchName": f"refs/heads/{branch}",
                  "$top": 1}

        builds = None
        try:
            builds = (await self.make_request("GET", endpoint, params=params))['value']
        except Exception:
            log.exception(f"Unable to fetch last pipelines build for {org}/{project}")
            pass
        # The API request should return one, and this method has to return one result
        if builds:
            builds = builds[0]
        return builds

    async def get_jobs_from_timeline(self, timeline_url: str) -> List[Job]:
        """
        Parse the timeline and get the jobs (phases) and their statuses.
        """
        records = (await self.make_request("GET", timeline_url,
                                           params={'api-version': "6.0"}))['records']
        phases = filter(lambda records: records['type'] == "Phase", records)
        # none is not allowed but is returned when a build is running
        return [Job(ph['name'],
                    "unknown" if not ph['result'] else ph['result']) for ph in phases]

    async def get_last_build(self,
                             org: str,
                             project: str,
                             branch: str) -> Build:
        """
        Get a reduced report about the last job,
        including the status of the individual jobs.
        """
        resp = await self.get_last_build_on_branch(org, project, branch)
        if resp:
            status = resp.get('result', 'unknown')
            last_time = datetime.fromisoformat(resp['startTime'].split(".")[0])
            if datetime.now() - last_time > timedelta(hours=32):
                status = "out-of-date"
            return Build(
                service_name="Azure Pipelines",
                url=resp['_links']['web']['href'],
                status=status,
                time=last_time,
                jobs=await self.get_jobs_from_timeline(resp['_links']['timeline']['href'])
            )
