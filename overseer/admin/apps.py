from django.contrib.admin.apps import AdminConfig


class OverseerAdminConfig(AdminConfig):
    default_site = 'overseer.admin.OverseerAdminSite'
