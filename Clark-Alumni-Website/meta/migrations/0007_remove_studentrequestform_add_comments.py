# Generated by Django 4.2.4 on 2023-11-10 03:44

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("meta", "0006_studentrequestform_add_comments"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="studentrequestform",
            name="add_comments",
        ),
    ]