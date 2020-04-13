"""
This file was generated with the customdashboard management command, it
contains the two classes for the main dashboard and app index dashboard.
You can customize these classes as you want.

To activate your index dashboard add the following to your settings.py::
    ADMIN_TOOLS_INDEX_DASHBOARD = 'app.dashboard.CustomIndexDashboard'

And to activate the app index dashboard::
    ADMIN_TOOLS_APP_INDEX_DASHBOARD = 'app.dashboard.CustomAppIndexDashboard'
"""

from admin_tools.dashboard import AppIndexDashboard, Dashboard, modules
from django.utils.translation import ugettext_lazy as _

from .modules import (
    PurloviaConfigModule,
    PurloviaLatestRunModule,
    PurloviaRunningModule,
    PurloviaSummaryModule,
)


class OverseerIndexDashboard(Dashboard):
    """
    Custom index dashboard for app.
    """

    def init_with_context(self, context):
        # append an app list module for "Applications"

        self.children.append(PurloviaSummaryModule())
        self.children.append(
            modules.Group(
                _("Data"),
                display="accordion",
                children=[
                    modules.AppList(
                        _("Celery"),
                        exclude=(
                            "django.contrib.*",
                            "overseer.users.*",
                            "overseer.purlovia.*",
                            "allauth.*",
                        ),
                    ),
                    modules.AppList(
                        _("Administration"),
                        models=(
                            "django.contrib.*",
                            "overseer.users.*",
                            "allauth.*",
                        ),
                    ),
                ],
            )
        )

        # append a recent actions module
        self.children.append(modules.RecentActions(_("Recent Actions"), 5))


class OverseerAppIndexDashboard(AppIndexDashboard):
    """
    Custom app index dashboard for app.
    """

    # we disable title because its redundant with the model list module
    title = ""

    def init_with_context(self, context):
        if self.get_id() == "purlovia-dashboard":
            self.title = self.app_title
            self.columns = 1
            self.children = [
                PurloviaSummaryModule(enabled=False),
                PurloviaConfigModule(),
                PurloviaLatestRunModule(),
                PurloviaRunningModule(),
            ]
        else:
            # append a model list module and a recent actions module
            self.children += [
                modules.ModelList(self.app_title, self.models),
                modules.RecentActions(
                    _("Recent Actions"),
                    include_list=self.get_app_content_types(),
                    limit=5,
                ),
            ]
