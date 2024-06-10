# Generated by Django 5.0.6 on 2024-06-02 20:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Todo",
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
                ("description", models.TextField()),
                (
                    "priority",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("A", "A"),
                            ("B", "B"),
                            ("C", "C"),
                            ("D", "D"),
                            ("E", "E"),
                            ("F", "F"),
                            ("G", "G"),
                            ("H", "H"),
                            ("I", "I"),
                            ("J", "J"),
                            ("K", "K"),
                            ("L", "L"),
                            ("M", "M"),
                            ("N", "N"),
                            ("O", "O"),
                            ("P", "P"),
                            ("Q", "Q"),
                            ("R", "R"),
                            ("S", "S"),
                            ("T", "T"),
                            ("U", "U"),
                            ("V", "V"),
                            ("W", "W"),
                            ("X", "X"),
                            ("Y", "Y"),
                            ("Z", "Z"),
                        ],
                        max_length=1,
                    ),
                ),
            ],
        ),
    ]