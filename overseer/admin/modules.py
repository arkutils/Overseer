from typing import Optional

from admin_tools.dashboard.modules import DashboardModule
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django_celery_results.models import TaskResult
from reversion.models import Version

from overseer.celery.utils import get_output_for_task
from overseer.purlovia.models import Config
from overseer.purlovia.tasks import (
    PURLOVIA_QUEUE_TASK_NAME,
    PURLOVIA_TASK_NAME,
    get_running_task,
)


class PurloviaModule(DashboardModule):
    _initialized: bool

    flower_url: str = settings.FLOWER_BASE_URL
    task_name: str = PURLOVIA_QUEUE_TASK_NAME

    def _initalize_data(self, request):
        pass

    def init_with_context(self, context):
        if self._initialized:
            return

        self._initalize_data(context["request"])

        self._initialized = True


class PurloviaLatestRunModule(PurloviaModule):
    last_completed: Optional[TaskResult] = None
    last_completed_output: Optional[str] = None

    template: str = "overseer/admin/dashboard/latest_run.html"
    title: str = _("Latest Run")

    def is_empty(self):
        return self.last_completed is None

    def _initalize_data(self, request):
        super()._initalize_data(request)

        # cache the last completed on the request object so other modules
        # can use it
        if not hasattr(request, "last_completed"):
            request.last_completed = (
                TaskResult.objects.filter(
                    task_name=PURLOVIA_TASK_NAME,
                    status__in=["SUCCESS", "FAILURE"],
                )
                .order_by("-date_done")
                .first()
            )

        self.last_completed = request.last_completed

    def init_with_context(self, context):
        if self._initialized:
            return

        self._initalize_data(context["request"])

        if self.last_completed:
            self.last_completed_output = "\n".join(
                get_output_for_task(self.last_completed)
            )

        self._initialized = True


class PurloviaRunningModule(PurloviaModule):
    last_started: Optional[TaskResult] = None
    last_started_output: Optional[str] = None
    can_start: bool = False

    template: str = "overseer/admin/dashboard/running.html"
    title: str = _("Current Run")

    def is_empty(self):
        return False

    def _initalize_data(self, request):
        super()._initalize_data(request)

        # cache the last started on the request object so other modules
        # can use it
        if not hasattr(request, "last_started"):
            request.last_started = get_running_task()

        self.last_started = request.last_started

        self.can_start = request.user.has_perm(
            "django_celery_results.view_task_result"
        )

    def init_with_context(self, context):
        if self._initialized:
            return

        self._initalize_data(context["request"])

        if self.last_started:
            self.last_started_output = "\n".join(
                get_output_for_task(self.last_started)
            )

        self._initialized = True


class PurloviaSummaryModule(PurloviaLatestRunModule, PurloviaRunningModule):
    _initialized: bool

    template: str = "overseer/admin/dashboard/purlovia_summary.html"
    title: str = _("Purlovia Overview")

    def is_empty(self):
        return False

    def init_with_context(self, context):
        if self._initialized:
            return

        self._initalize_data(context["request"])

        self._initialized = True


class PurloviaConfigModule(PurloviaModule):
    _initialized: bool

    config: Optional[Config] = None
    config_version: Optional[Config] = None

    template: str = "overseer/admin/dashboard/config.html"
    title: str = _("Config")

    def is_empty(self):
        return False

    def _initalize_data(self, request):
        super()._initalize_data(request)

        self.config = Config.load()
        self.config_version = Version.objects.get_for_object(
            self.config
        ).first()
