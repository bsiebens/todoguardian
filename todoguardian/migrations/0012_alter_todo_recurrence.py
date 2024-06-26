# Generated by Django 5.0.6 on 2024-06-11 21:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("todoguardian", "0011_remove_todo_completed_todo__completed"),
    ]

    operations = [
        migrations.AlterField(
            model_name="todo",
            name="recurrence",
            field=models.CharField(
                blank=True,
                help_text="Recurrence can be defined as a string ([0-9][bdwmy]), add + in front to have strict recurrence.",
                max_length=5,
                null=True,
            ),
        ),
    ]
