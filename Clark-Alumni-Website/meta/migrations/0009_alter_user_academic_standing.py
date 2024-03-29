# Generated by Django 4.2.4 on 2024-01-15 20:41

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("meta", "0008_alter_user_academic_standing"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="academic_standing",
            field=models.CharField(
                choices=[
                    ("first_year", "First Year"),
                    ("sophomore", "Sophomore"),
                    ("junior", "Junior"),
                    ("senior", "Senior"),
                    ("grad", "Grad Student"),
                    ("alumni", "Alum"),
                ],
                null=True,
            ),
        ),
    ]
