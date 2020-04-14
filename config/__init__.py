from automate.config.reader import read_config
from automate.config.sections import ConfigFile

__all__ = [
    "get_global_config",
    "force_reload",
    "ConfigFile",
    "OVERRIDE_FILENAME",
    "LOGGING_FILENAME",
    "HIERARCHY_FILENAME",
    "ROOT_LOGGER",
]

DEFAULT_CONFIG_FILENAME = "/app/overseer/purlovia/config/config.default.ini"
OVERRIDE_FILENAME = "/app/overseer/purlovia/config/overrides.yaml"
LOGGING_FILENAME = "/app/overseer/purlovia/config/logging.yaml"
HIERARCHY_FILENAME = "/app/overseer/purlovia/config/hierarchy.yaml"
ROOT_LOGGER = "celery.task."
DO_SIMPLE_RUN = True


def get_global_config() -> ConfigFile:
    # make sure current task is loaded at runtime
    # pylint: disable=import-outside-toplevel
    from celery import current_task
    from overseer.purlovia.models import Config
    from django.core.cache import cache

    config = None
    if current_task is not None:
        config = cache.get(f"config.{current_task.request.id}")

    if config is None:
        config = read_config(config_string=Config.load().config)

        if current_task is not None:
            cache.set(f"config.{current_task.request.id}", config, 43200)

    return config
