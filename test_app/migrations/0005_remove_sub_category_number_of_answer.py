# Generated by Django 4.1.7 on 2023-05-08 04:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("test_app", "0004_alter_sub_category_name"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="sub_category",
            name="number_of_answer",
        ),
    ]
