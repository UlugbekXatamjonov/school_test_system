# Generated by Django 4.1.7 on 2023-03-24 04:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("test_app", "0002_delete_result"),
        ("user_app", "0002_student_student_tests_result"),
    ]

    operations = [
        migrations.AlterField(
            model_name="student",
            name="student_tests",
            field=models.ManyToManyField(
                blank=True, related_name="student_tests", to="test_app.sub_category"
            ),
        ),
    ]
