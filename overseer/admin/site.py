from copy import deepcopy

from django.contrib.admin.sites import AdminSite
from django.db.models.base import ModelBase
from django.urls import path

from . import views


class OverseerAdminSite(AdminSite):
    def register(self, model_or_iterable, admin_class=None, **options):
        if isinstance(model_or_iterable, ModelBase):
            model_or_iterable = [model_or_iterable]

        to_register = []
        for model in model_or_iterable:
            if hasattr(model, "admin_app_label"):
                model_copy = deepcopy(model)
                model_copy._meta.app_label = model.admin_app_label
                to_register.append(model_copy)
            else:
                to_register.append(model)

        return super().register(to_register, admin_class, **options)

    def get_urls(self):
        urls = super().get_urls()

        overseer_urls = [
            path(
                "task/start/<str:task_name>/",
                views.StartTaskView.as_view(),
                name="start_task",
            )
        ]

        return overseer_urls + urls

    def each_context(self, request):
        # Django not loaded until here
        # pylint: disable=import-outside-toplevel
        from overseer.purlovia.models import Config

        Config.load()

        return super().each_context(request)
