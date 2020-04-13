import ue.context
from automate.run import run
from celery import current_app
from celery.utils.log import get_task_logger
from django.core.cache import cache

from config import DO_SIMPLE_RUN, get_global_config
from config.celery_app import app

logger = get_task_logger(__name__)


PURLOVIA_QUEUE_TASK_NAME = "overseer.purlovia.tasks.automate_queue"
PURLOVIA_TASK_NAME = "overseer.purlovia.tasks.automate"
PURLOVIA_LOCK_NAME = "overseer_task.automate"


class AlreadyRunning(Exception):
    pass


def get_running_task():
    # Django not loaded until here
    # pylint: disable=import-outside-toplevel
    from django_celery_results.models import TaskResult

    task = (
        TaskResult.objects.filter(
            task_name=PURLOVIA_TASK_NAME, status="STARTED"
        )
        .order_by("-date_done")
        .first()
    )

    if task is None:
        logger.info("Purlovia is not running")
        return None

    i = current_app.control.inspect()

    found = False
    active_dict = i.active() or {}

    for tasks in active_dict.values():
        for task_dict in tasks:
            if task_dict["id"] == task.task_id:
                found = True

    if not found:
        TaskResult.objects.filter(
            task_name=PURLOVIA_TASK_NAME, status="STARTED"
        ).delete()

        logger.info("Cleaning up previous started task")
        return None

    logger.info("Purlovia is running")
    return task


@app.task()
def automate():
    lock = cache.lock(PURLOVIA_LOCK_NAME)

    acquired = lock.acquire(blocking=True, timeout=1)

    if acquired:
        try:
            ue.context.disable_metadata()

            config = get_global_config()
            logger.info("DEV mode enabled")
            config.git.UseIdentity = False
            config.git.SkipCommit = True
            config.git.SkipPush = True
            config.errors.SendNotifications = False
            config.dev.DevMode = True

            if DO_SIMPLE_RUN:
                config.run_sections = {"asb.species": True}

            run(config)
        finally:
            lock.release()
    else:
        raise AlreadyRunning()


@app.task()
def automate_queue():
    task = get_running_task()

    if task is None:
        lock = cache.lock(PURLOVIA_LOCK_NAME)
        if lock.locked():
            logger.info("Reseting lock...")
            lock.reset()

        logger.info("Starting automate...")
        return automate.delay()
    else:
        raise AlreadyRunning()
