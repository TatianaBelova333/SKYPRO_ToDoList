# Generated by Django 4.1.1 on 2022-10-27 17:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("goals", "0005_alter_goalcategory_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="goal",
            name="description",
            field=models.TextField(
                blank=True, default=None, null=True, verbose_name="Описание"
            ),
        ),
    ]
