import copy
from typing import Dict, NamedTuple

from health_check.plugins import plugin_dir


class HealthCheckResult(NamedTuple):
    checks: Dict[str, str]
    passing: bool


class HealthCheckHandler:
    @classmethod
    def get_plugins(cls):
        return sorted(
            (
                plugin_class(**copy.deepcopy(options))
                for plugin_class, options in plugin_dir._registry
            ),
            key=lambda plugin: plugin.identifier(),
        )

    @classmethod
    def run_all_checks(cls) -> HealthCheckResult:
        """
        The health_check library provides its own template and view. However, it has
        bugs, runs health checks in threads which causes further problems and does
        not fit into our DRF based authentication. We just use this library
        for the nice suite of health check plugins it provides, and use its python
        API to run those in a simpler and safer fashion in this method.
        """

        checks = {}

        passing = True
        for plugin in cls.get_plugins():
            # The plugin checks can fail and raise but we always want to catch
            # to report back that they failed.
            # noinspection PyBroadException
            try:
                plugin.run_check()
            except Exception:  # nosec
                pass
            checks[str(plugin.identifier())] = str(plugin.pretty_status())
            if plugin.critical_service and not plugin.status:
                passing = False

        return HealthCheckResult(checks, passing)
