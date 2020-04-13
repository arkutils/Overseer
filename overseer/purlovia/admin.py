from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.conf.urls import url
from django.contrib import admin, messages
from django.contrib.admin.options import csrf_protect_m
from django.core.exceptions import PermissionDenied
from django.forms.models import model_to_dict
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.utils.translation import ugettext_lazy as _
from djangocodemirror.fields import CodeMirrorField
from reversion.admin import VersionAdmin
from reversion.revisions import set_comment

from .models import Config


class ConfigRevisionForm(forms.ModelForm):
    class Meta:
        model = Config
        fields = "__all__"

    config = CodeMirrorField(
        label=_("Config"), required=True, config_name="properties"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()

        self.helper.add_input(Submit("submit", "Save"))


class ConfigForm(ConfigRevisionForm):
    message = forms.CharField(
        label=_("Change Message"),
        widget=forms.Textarea(attrs={"cols": 120, "rows": 10}),
    )

    def save(self):
        config = Config.load()

        config.config = self.cleaned_data["config"]
        config.save()
        set_comment(self.cleaned_data["message"])


@admin.register(Config)
class ConfigAdmin(VersionAdmin):
    change_list_template = "overseer/purlovia/config_form.html"
    change_list_form = ConfigForm
    form = ConfigRevisionForm
    object_history_template = "overseer/purlovia/object_history.html"
    revision_form_template = "overseer/purlovia/revision_form.html"

    def get_urls(self):
        return [
            url(
                r"^$",
                self.admin_site.admin_view(self.changelist_view),
                name="purlovia_config_changelist",
            ),
            url(
                r"^$",
                self.admin_site.admin_view(self.changelist_view),
                name="purlovia_config_add",
            ),
            url(
                r"^([^/]+)/history/$",
                self.admin_site.admin_view(self.history_view),
                name="purlovia_config_history",
            ),
            url(
                r"^([^/]+)/history/(\d+)/$",
                self.admin_site.admin_view(self.revision_view),
                name="purlovia_config_revision",
            ),
        ]

    def get_changelist_form(self, request, **kwargs):
        """
        Returns a Form class for use in the changelist_view.
        """
        # Defaults to self.change_list_form in order to preserve backward
        # compatibility
        return self.change_list_form

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    @csrf_protect_m
    def changelist_view(self, request, extra_context=None):
        with self.create_revision(request):
            if not self.has_change_permission(request, None):
                raise PermissionDenied

            initial = model_to_dict(Config.load(), fields=("config",))
            form_cls = self.get_changelist_form(request)
            form = form_cls(initial=initial)

            if request.method == "POST":
                form = form_cls(
                    data=request.POST, files=request.FILES, initial=initial
                )
                if form.is_valid():
                    form.save()

                    messages.add_message(
                        request,
                        messages.SUCCESS,
                        _("Purlova settings updated successfully."),
                    )
                    return HttpResponseRedirect(".")

            context = dict(
                self.admin_site.each_context(request),
                config_values=[],
                title=self.model._meta.app_config.verbose_name,
                app_label="purlovia",
                opts=self.model._meta,
                form=form,
                media=self.media + form.media,
                icon_type="svg",
            )

            return TemplateResponse(
                request, self.change_list_template, context
            )
