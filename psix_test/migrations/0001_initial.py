# Generated by Django 4.1.7 on 2023-05-25 07:33

import autoslug.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="PSTSub_Category",
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
                (
                    "name",
                    models.CharField(
                        max_length=200, unique=True, verbose_name="Kategoriya nomi"
                    ),
                ),
                (
                    "slug",
                    autoslug.fields.AutoSlugField(
                        editable=False, populate_from="name", unique=True
                    ),
                ),
                (
                    "description",
                    models.CharField(
                        blank=True,
                        max_length=350,
                        null=True,
                        verbose_name="Kategoriya haqida",
                    ),
                ),
                (
                    "number_of_questions",
                    models.PositiveIntegerField(
                        blank=True, default=0, null=True, verbose_name="Savollar soni"
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[("active", "Faol"), ("deactive", "Faol emas")],
                        default="active",
                        max_length=100,
                        verbose_name="Holati",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now=True)),
                ("updated_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "verbose_name": "Kategoriya",
                "verbose_name_plural": "Kategoriyalar",
                "ordering": ("-created_at", "status"),
            },
        ),
        migrations.CreateModel(
            name="Question",
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
                (
                    "question",
                    models.CharField(max_length=350, verbose_name="Savol matni"),
                ),
                (
                    "slug",
                    autoslug.fields.AutoSlugField(
                        editable=False, populate_from="question", unique=True
                    ),
                ),
                (
                    "job_type",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("no", "Yo'q"),
                            ("tabiat", "Tabiat"),
                            ("texnika", "texnika"),
                            ("belgi", "Belgi"),
                            ("sanat", "San'at"),
                            ("inson", "Inson"),
                        ],
                        default="no",
                        max_length=100,
                        null=True,
                        verbose_name="Kasb turi",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[("active", "Faol"), ("deactive", "Faol emas")],
                        default="active",
                        max_length=100,
                        verbose_name="Holati",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now=True)),
                ("updated_at", models.DateTimeField(auto_now_add=True)),
                (
                    "category_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="pstquestion",
                        to="psix_test.pstsub_category",
                        verbose_name="Kategoriya",
                    ),
                ),
            ],
            options={
                "verbose_name": "Savol",
                "verbose_name_plural": "Savollar",
                "ordering": ("-created_at", "status"),
            },
        ),
        migrations.CreateModel(
            name="Answer",
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
                (
                    "answer",
                    models.CharField(
                        blank=True, max_length=350, null=True, verbose_name="Variant"
                    ),
                ),
                (
                    "slug",
                    autoslug.fields.AutoSlugField(
                        editable=False, populate_from="answer", unique=True
                    ),
                ),
                (
                    "true_answer",
                    models.BooleanField(
                        blank=True,
                        default=False,
                        null=True,
                        verbose_name="To'g'ri javob",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[("active", "Faol"), ("deactive", "Faol emas")],
                        default="active",
                        max_length=100,
                        verbose_name="Holati",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now=True)),
                ("updated_at", models.DateTimeField(auto_now_add=True)),
                (
                    "question_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="answer",
                        to="psix_test.question",
                        verbose_name="Savol",
                    ),
                ),
            ],
            options={
                "verbose_name": "Javob",
                "verbose_name_plural": "Javoblar",
                "ordering": ("-created_at", "status"),
            },
        ),
    ]
