"""
This file was generated with the custommenu management command, it contains
the classes for the admin menu, you can customize this class as you want.

To activate your custom menu add the following to your settings.py::
    ADMIN_TOOLS_MENU = 'app.menu.CustomMenu'
"""

from admin_tools.menu import Menu, items
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _


class OverseerMenu(Menu):
    """
    Custom Menu for app admin site.
    """

    def __init__(self, **kwargs):
        Menu.__init__(self, **kwargs)
        self.children += [
            items.MenuItem(_("Overseer"), reverse("admin:index")),
            items.Bookmarks(),
            items.MenuItem(
                _("Purlovia"), reverse("admin:app_list", args=("purlovia",)),
            ),
            items.AppList(
                _("Data"),
                exclude=(
                    "django.contrib.*",
                    "overseer.users.*",
                    "overseer.purlovia.*",
                    "allauth.*",
                ),
            ),
            items.AppList(
                _("Administration"),
                models=("django.contrib.*", "overseer.users.*", "allauth.*"),
            ),
        ]
