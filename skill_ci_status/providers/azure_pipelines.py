"""
Functions for interacting with the Azure Pipelines API.
"""
from typing import List

from .base import BaseProvider, BuildReport, JobReport


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

        return (await self.make_request("GET", endpoint, params=params))['value'][0]

    async def get_jobs_from_timeline(self, timeline_url: str) -> List[JobReport]:
        """
        Parse the timeline and get the jobs (phases) and their statuses.
        """
        records = (await self.make_request("GET", timeline_url,
                                           params={'api-version': "6.0"}))['records']
        phases = filter(lambda records: records['type'] == "Phase", records)
        return [JobReport(ph['name'], ph['result']) for ph in phases]

    async def get_last_build_report(self,
                                    org: str,
                                    project: str,
                                    branch: str) -> BuildReport:
        """
        Get a reduced report about the last job,
        including the status of the individual jobs.
        """
        resp = await self.get_last_build_on_branch(org, project, branch)
        return BuildReport(
            status=resp['result'],
            badge=resp['_links']['badge']['href'],
            build=resp['_links']['web']['href'],
            jobs=await self.get_jobs_from_timeline(resp['_links']['timeline']['href'])
        )
