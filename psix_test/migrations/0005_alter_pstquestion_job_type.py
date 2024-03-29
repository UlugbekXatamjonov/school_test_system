# Generated by Django 4.1.7 on 2023-05-26 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("psix_test", "0004_remove_pstanswer_job"),
    ]

    operations = [
        migrations.AlterField(
            model_name="pstquestion",
            name="job_type",
            field=models.CharField(
                blank=True,
                choices=[
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
    ]
