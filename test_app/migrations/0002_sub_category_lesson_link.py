# Generated by Django 4.1.7 on 2023-05-06 05:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("test_app", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="sub_category",
            name="lesson_link",
            field=models.CharField(
                blank=True, max_length=300, null=True, verbose_name="Dars uchun link"
            ),
        ),
    ]
