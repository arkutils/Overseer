# Generated by Django 3.0.5 on 2020-04-13 21:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Config",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("config", models.TextField(verbose_name="Config")),
                ("last_updated", models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
