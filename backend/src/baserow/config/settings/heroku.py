from .base import *  # noqa: F403, F401

# Set the limit of the connection pool based on the amount of workers that must be
# started with a limit of 10, which is the default value. This is needed because the
# `heroku-redis:mini` doesn't accept more than 20 connections.
CELERY_BROKER_POOL_LIMIT = min(
    4 * int(os.getenv("BASEROW_AMOUNT_OF_WORKERS", "1")), 10  # noqa: F405
)
CELERY_REDIS_MAX_CONNECTIONS = min(
    4 * int(os.getenv("BASEROW_AMOUNT_OF_WORKERS", "1")), 10  # noqa: F405
)

HEROKU_ENABLED = True
