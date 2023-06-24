# Generated by Django 4.1.7 on 2023-03-17 08:10

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("buildings", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Amenity",
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
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("updated_on", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=100)),
                (
                    "actor",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ["-id"],
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Restroom",
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
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("updated_on", models.DateTimeField(auto_now=True)),
                (
                    "gender",
                    models.CharField(
                        choices=[
                            ("male", "male"),
                            ("female", "female"),
                            ("unisex", "unisex"),
                        ],
                        max_length=32,
                    ),
                ),
                (
                    "actor",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                ("amenities", models.ManyToManyField(to="restrooms.amenity")),
                (
                    "building",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="buildings.building",
                    ),
                ),
                (
                    "floor",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="buildings.floor",
                    ),
                ),
            ],
            options={
                "ordering": ["-id"],
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="ToiletType",
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
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("updated_on", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=100)),
                (
                    "actor",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ["-id"],
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="RestroomToiletType",
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
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("updated_on", models.DateTimeField(auto_now=True)),
                ("count", models.PositiveIntegerField()),
                (
                    "actor",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "restroom",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="restrooms.restroom",
                    ),
                ),
                (
                    "toilet_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="restrooms.toilettype",
                    ),
                ),
            ],
            options={
                "ordering": ["-id"],
                "abstract": False,
            },
        ),
        migrations.AddField(
            model_name="restroom",
            name="toilet_types",
            field=models.ManyToManyField(
                through="restrooms.RestroomToiletType", to="restrooms.toilettype"
            ),
        ),
    ]