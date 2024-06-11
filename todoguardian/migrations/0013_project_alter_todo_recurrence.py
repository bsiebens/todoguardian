# Generated by Django 5.0.6 on 2024-06-11 21:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("todoguardian", "0012_alter_todo_recurrence"),
    ]

    operations = [
        migrations.CreateModel(
            name="Project",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=250)),
            ],
            options={
                "ordering": ["name"],
            },
        ),
        migrations.AlterField(
            model_name="todo",
            name="recurrence",
            field=models.CharField(
                blank=True,
                default="",
                help_text="Recurrence can be defined as a string ([0-9][bdwmy]), add + in front to have strict recurrence.",
                max_length=5,
            ),
            preserve_default=False,
        ),
    ]
