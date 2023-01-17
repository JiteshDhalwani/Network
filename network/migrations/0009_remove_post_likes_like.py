# Generated by Django 4.1.4 on 2022-12-30 18:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("network", "0008_alter_follow_unique_together"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="post",
            name="likes",
        ),
        migrations.CreateModel(
            name="Like",
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
                (
                    "post",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="post_liked",
                        to="network.post",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="user_liked",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
