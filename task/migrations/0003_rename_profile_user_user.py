# Generated by Django 4.2.5 on 2023-09-29 16:40

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("task", "0002_rename_user_user_profile"),
    ]

    operations = [
        migrations.RenameField(
            model_name="user",
            old_name="profile",
            new_name="user",
        ),
    ]
