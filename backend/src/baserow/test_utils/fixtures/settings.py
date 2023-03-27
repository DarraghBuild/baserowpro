from django.core.cache import cache

from baserow.core.constants import SETTINGS_CACHE_KEY
from baserow.core.models import Settings


class SettingsFixtures:
    def update_settings(self, **kwargs):
        settings, created = Settings.objects.update_or_create(defaults=kwargs)
        cache.delete(SETTINGS_CACHE_KEY)
        return settings
