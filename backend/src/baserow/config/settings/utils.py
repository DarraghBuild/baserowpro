import os
import traceback
from typing import Any, Callable, List, NamedTuple, Optional, Union

from celery.schedules import crontab
from redis.asyncio.connection import Connection, RedisSSLContext


def setup_dev_e2e(*args, **kwargs):
    # noinspection PyBroadException
    try:
        from django.contrib.auth import get_user_model

        from baserow.core.db import LockedAtomicTransaction

        User = get_user_model()

        from baserow.core.models import Settings

        with LockedAtomicTransaction(Settings):
            setup_dev_e2e_users_and_instance_id(User, args, kwargs)
    except Exception:  # nosec
        traceback.print_exc()
        print("ERROR setting up dev e2e env, see above for stack.")
        pass


def setup_dev_e2e_users_and_instance_id(User, args, kwargs):
    """
    Responsible for changing the `Setting.instance_id` to "1" and creating
    two "staff" base user accounts on post_migrate.
    """

    from baserow.core.models import Settings

    if Settings.objects.get().instance_id != "1":
        from baserow.core.user.handler import UserHandler

        user_handler = UserHandler()
        from baserow.core.user.exceptions import UserAlreadyExist

        for email in ["dev@baserow.io", "e2e@baserow.io"]:
            uname = email.split("@")[0]
            try:
                user = user_handler.create_user(f"staff-{uname}", email, "testpassword")
            except UserAlreadyExist:
                user = User.objects.get(email=email)
            user.is_staff = True
            user.save()

        Settings.objects.update(instance_id="1")


class Setting(NamedTuple):
    """
    Describes how an environment variable should be read, parsed and setup.
    """

    name: str
    parser: Optional[Callable[[str], Any]] = None
    default: Optional[Any] = None
    setting_name: Optional[str] = None


def read_file(file_path):
    with open(file_path, "r") as file:
        file_contents = file.read()
    return file_contents


def set_settings_from_env_if_present(
    settings_module, settings: List[Union[str, Setting]]
):
    """
    Takes a list of strings or Setting named tuples, reads in the environment variable
    with the same name for each and then sets the Django setting with the same name.

    Use the Setting NamedTuple if you want to specify a parser for the env var or
    a default value. Otherwise, just provide strings which match the env var/setting
    name.
    """

    for s in settings:
        if type(s) is str:
            set_setting_from_env_if_present(settings_module, s, s)
        else:
            set_setting_from_env_if_present(
                settings_module, s.name, s.setting_name or s.name, s.parser, s.default
            )


def set_setting_from_env_if_present(
    settings_module,
    env_var: str,
    setting_name: str,
    parser: Optional[Callable[[str], Any]] = None,
    default: Any = None,
):
    value = os.getenv(env_var, None)
    if value is not None and parser is not None:
        value = parser(value)
    elif value is None:
        value = default

    if value is not None:
        settings_module[setting_name] = value


def str_to_bool(s: str) -> bool:
    return s.lower().strip() in ("y", "yes", "t", "true", "on", "1")


def get_crontab_from_env(env_var_name: str, default_crontab: str) -> crontab:
    """
    Parses a crontab from an environment variable if present or instead uses the
    default.

    Celeries crontab constructor takes the arguments in a different order than the
    actual crontab spec so we expand and re-order the arguments to match.
    """

    minute, hour, day_of_month, month_of_year, day_of_week = os.getenv(
        env_var_name, default_crontab
    ).split(" ")
    return crontab(minute, hour, day_of_week, day_of_month, month_of_year)


# Required to get Channels v4 working with Heroku Redis
# See https://github.com/django/channels_redis/issues/235
class CustomSSLConnection(Connection):
    def __init__(
        self,
        ssl_context: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.ssl_context = RedisSSLContext(ssl_context)


class RedisSSLContext:  # noqa: F811
    __slots__ = ("context",)

    def __init__(
        self,
        ssl_context,
    ):
        self.context = ssl_context

    def get(self):
        return self.context
