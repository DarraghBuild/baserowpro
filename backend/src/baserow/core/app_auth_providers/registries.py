from baserow.core.registry import (
    APIUrlsRegistryMixin,
    CustomFieldsRegistryMixin,
    MapAPIExceptionsInstanceMixin,
    ModelRegistryMixin,
    Registry,
)


class AppAuthenticationProviderTypeRegistry(
    MapAPIExceptionsInstanceMixin,
    APIUrlsRegistryMixin,
    ModelRegistryMixin,
    CustomFieldsRegistryMixin,
    Registry,
):
    """
    With the authentication provider registry it is possible to register new
    authentication providers. An authentication provider is an abstraction made
    specifically for Baserow. If added to the registry a user can use that
    authentication provider to login.
    """

    name = "app_auth_provider"


app_auth_provider_type_registry = AppAuthenticationProviderTypeRegistry()
