# Generated by Django 4.2.5 on 2023-10-02 18:23

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("task", "0005_remove_image_url"),
    ]

    operations = [
        migrations.AlterField(
            model_name="image",
            name="image",
            field=models.ImageField(null=True, upload_to="images/"),
        ),
    ]
