# Generated by Django 5.0.6 on 2024-06-11 20:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("todoguardian", "0009_delete_todoold"),
    ]

    operations = [
        migrations.AddField(
            model_name="todo",
            name="completed",
            field=models.BooleanField(default=False),
        ),
    ]
