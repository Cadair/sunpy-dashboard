from .azure_pipelines import AzureProvider

__all__ = ['providers']

supported_providers = {"azure": AzureProvider}
