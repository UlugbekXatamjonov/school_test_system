# Generated by Django 4.1.7 on 2023-05-26 06:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user_app", "0002_pstresult"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="pstresult",
            name="tashxis",
        ),
        migrations.AddField(
            model_name="pstresult",
            name="job",
            field=models.CharField(
                blank=True, max_length=25, null=True, verbose_name="kasb"
            ),
        ),
    ]
