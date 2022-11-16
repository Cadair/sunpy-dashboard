from .azure_pipelines import AzureProvider
from .github_actions import GitHubProvider

__all__ = ['providers']

supported_providers = {"azure": AzureProvider, "github": GitHubProvider}
