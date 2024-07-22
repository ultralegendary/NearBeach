# Generated by Django 5.0.7 on 2024-07-22 10:04

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("NearBeach", "0028_userjob_job_sort_number"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name="userjob",
            name="job_date",
            field=models.DateField(),
        ),
        migrations.CreateModel(
            name="ObjectTemplate",
            fields=[
                (
                    "object_template_id",
                    models.BigAutoField(primary_key=True, serialize=False),
                ),
                (
                    "object_template_type",
                    models.IntegerField(choices=[(0, "project"), (1, "task")]),
                ),
                ("object_template_json", models.JSONField()),
                ("date_created", models.DateTimeField(auto_now_add=True)),
                ("date_modified", models.DateTimeField(auto_now=True)),
                ("is_deleted", models.BooleanField(default=False)),
                (
                    "change_user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="%(class)s_change_user",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ObjectTemplateGroup",
            fields=[
                (
                    "object_template_group_id",
                    models.BigAutoField(primary_key=True, serialize=False),
                ),
                ("date_created", models.DateTimeField(auto_now_add=True)),
                ("date_modified", models.DateTimeField(auto_now=True)),
                ("is_deleted", models.BooleanField(default=False)),
                (
                    "change_user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="%(class)s_change_user",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "group",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="NearBeach.group",
                    ),
                ),
                (
                    "object_template",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="NearBeach.objecttemplate",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ScheduledObject",
            fields=[
                (
                    "schedule_object_id",
                    models.BigAutoField(primary_key=True, serialize=False),
                ),
                ("last_run", models.DateField(blank=True, null=True)),
                ("start_date", models.DateField()),
                ("end_date", models.DateField(blank=True, null=True)),
                ("next_scheduled_run", models.DateField(blank=True, null=True)),
                ("number_of_repeats", models.IntegerField(default=-1)),
                ("run_count", models.IntegerField(default=0)),
                ("is_active", models.BooleanField(default=True)),
                (
                    "frequency",
                    models.CharField(
                        choices=[
                            ("Set Day of the Week", "Set Day of the Week"),
                            ("Weekly", "Weekly"),
                            ("Fortnightly", "Fortnightly"),
                            ("Monthly", "Monthly"),
                            ("Start of the Month", "Start of the Month"),
                            ("End of the Month", "End of the Month"),
                            (
                                "X Days before End of the Month",
                                "X Days before End of the Month",
                            ),
                        ],
                        max_length=50,
                    ),
                ),
                ("frequency_attribute", models.JSONField(blank=True, null=True)),
                ("date_created", models.DateTimeField(auto_now_add=True)),
                ("date_modified", models.DateTimeField(auto_now=True)),
                ("is_deleted", models.BooleanField(default=False)),
                (
                    "change_user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="%(class)s_change_user",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "object_template",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="NearBeach.objecttemplate",
                    ),
                ),
            ],
        ),
    ]
