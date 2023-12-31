# Generated by Django 4.2.5 on 2023-10-05 17:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("task", "0006_alter_image_image"),
    ]

    operations = [
        migrations.CreateModel(
            name="Tier",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=50, unique=True)),
                ("height", models.IntegerField(max_length=50)),
                ("orginal_link", models.BooleanField()),
            ],
        ),
        migrations.AlterField(
            model_name="user",
            name="tier",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.DO_NOTHING, to="task.tier"
            ),
        ),
    ]
