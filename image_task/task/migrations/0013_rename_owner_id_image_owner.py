# Generated by Django 4.2.5 on 2023-10-07 19:21

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("task", "0012_alter_image_name"),
    ]

    operations = [
        migrations.RenameField(
            model_name="image",
            old_name="owner_id",
            new_name="owner",
        ),
    ]