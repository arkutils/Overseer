import logging
import ue.context
from automate.run import run
from celery.utils.log import get_task_logger

from config import get_global_config
from config.celery_app import app

logger = get_task_logger(__name__)


@app.task()
def automate():
    ue.context.disable_metadata()

    config = get_global_config()
    logger.info("DEV mode enabled")
    config.git.UseIdentity = False
    config.git.SkipCommit = True
    config.git.SkipPush = True
    config.errors.SendNotifications = False
    config.dev.DevMode = True
    run(config)
