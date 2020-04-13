from typing import Optional

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

CONFIG_FILENAME = "/app/purlovia/config.ini"
OVERRIDE_FILENAME = "/app/purlovia/overrides.yaml"
LOGGING_FILENAME = "/app/purlovia/logging.yaml"
HIERARCHY_FILENAME = "/app/purlovia/hierarchy.yaml"
ROOT_LOGGER = "celery.task."
DO_SIMPLE_RUN = True

config: Optional[ConfigFile] = None


def get_global_config() -> ConfigFile:
    _ensure_loaded()
    assert config is not None  # nosec
    return config


def force_reload():
    global config  # pylint: disable=global-statement
    config = None
    _ensure_loaded()


def _ensure_loaded():
    global config  # pylint: disable=global-statement
    if not config:
        config = read_config(CONFIG_FILENAME)
