from django.db import models
from django.utils.translation import ugettext
from django.utils.translation import ugettext_lazy as _
from reversion.revisions import create_revision, set_comment

from config import DEFAULT_CONFIG_FILENAME


class Config(models.Model):
    config = models.TextField(_("Config"))
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return ugettext("Purlovia Config")

    # pylint: disable=arguments-differ
    def save(self, *args, **kwargs):
        # only a single config instance exists
        self.pk = 1
        super().save(*args, **kwargs)

    # pylint: disable=arguments-differ
    def delete(self, *args, **kwargs):
        # config cannot be deleted
        pass

    @classmethod
    def load(cls, force_load=False):
        obj, created = cls.objects.get_or_create(pk=1)

        if created or force_load:
            with open(DEFAULT_CONFIG_FILENAME, "r") as f:
                with create_revision():
                    obj.config = f.read()
                    set_comment("Loaded from default config")
                    obj.save()

        return obj
