import time

from django.contrib.auth.decorators import permission_required
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View

from overseer.purlovia.tasks import PURLOVIA_QUEUE_TASK_NAME, automate_queue

STARTABLE_TASKS = {PURLOVIA_QUEUE_TASK_NAME: automate_queue}


@method_decorator(
    permission_required("django_celery_results.view_task_result"),
    name="dispatch",
)
class StartTaskView(View):
    def get(self, request, task_name):
        # Django not loaded until here
        # pylint: disable=import-outside-toplevel
        from django_celery_results.models import TaskResult

        if task_name not in STARTABLE_TASKS:
            raise Http404(f"Task {task_name} does not exist")

        task = STARTABLE_TASKS[task_name]()
        # we have to give the task time you actually start
        time.sleep(1)

        try:
            task_result = TaskResult.objects.get(task_id=task.task_id)
        except TaskResult.DoesNotExist:
            return HttpResponseRedirect(reverse("admin:index"))

        return HttpResponseRedirect(
            reverse(
                "admin:django_celery_results_taskresult_change",
                args=(task_result.id,),
            ),
        )
