from django.contrib.admin.sites import AdminSite
from django.db.models.base import ModelBase


class OverseerAdminSite(AdminSite):
    def register(self, model_or_iterable, admin_class=None, **options):
        if isinstance(model_or_iterable, ModelBase):
            model_or_iterable = [model_or_iterable]

        for model in model_or_iterable:
            if hasattr(model, "admin_app_label"):
                model._meta.app_label = model.admin_app_label

        return super().register(model_or_iterable, admin_class, **options)
