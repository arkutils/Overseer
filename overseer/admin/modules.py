from typing import Optional

from admin_tools.dashboard.modules import DashboardModule
from django.utils.translation import ugettext_lazy as _
from django_celery_results.models import TaskResult

PURLOVIA_TASK_NAME = "overseer.purlovia.tasks.automate"


class PurloviaModule(DashboardModule):
    _initialized: bool

    last_started: Optional[TaskResult] = None
    last_completed: Optional[TaskResult] = None
    template = "overseer/admin/dashboard/purlovia.html"
    title: str = _("Purlovia")

    def is_empty(self):
        return False

    def init_with_context(self, context):
        if self._initialized:
            return

        self.last_started = (
            TaskResult.objects.filter(
                task_name=PURLOVIA_TASK_NAME, status="STARTED"
            )
            .order_by("-date_done")
            .first()
        )
        self.last_completed = (
            TaskResult.objects.filter(
                task_name=PURLOVIA_TASK_NAME, status__in=["SUCCESS", "FAILURE"]
            )
            .order_by("-date_done")
            .first()
        )

        self._initialized = True
