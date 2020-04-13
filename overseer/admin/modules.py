from typing import Optional

from admin_tools.dashboard.modules import DashboardModule
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django_celery_results.models import TaskResult

from overseer.purlovia.tasks import (
    PURLOVIA_QUEUE_TASK_NAME,
    PURLOVIA_TASK_NAME,
    get_running_task,
)


class PurloviaModule(DashboardModule):
    _initialized: bool

    last_started: Optional[TaskResult] = None
    last_completed: Optional[TaskResult] = None
    flower_url: str = settings.FLOWER_BASE_URL
    template: str = "overseer/admin/dashboard/purlovia.html"
    task_name: str = PURLOVIA_QUEUE_TASK_NAME
    can_start: bool = False
    title: str = _("Purlovia")

    def is_empty(self):
        return False

    def init_with_context(self, context):
        if self._initialized:
            return

        self.last_started = get_running_task()
        self.last_completed = (
            TaskResult.objects.filter(
                task_name=PURLOVIA_TASK_NAME,
                status__in=["SUCCESS", "FAILURE"],
            )
            .order_by("-date_done")
            .first()
        )

        self.can_start = context["request"].user.has_perm(
            "django_celery_results.view_task_result"
        )

        self._initialized = True
