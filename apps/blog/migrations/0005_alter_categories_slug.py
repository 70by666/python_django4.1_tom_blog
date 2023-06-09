# Generated by Django 4.1.7 on 2023-03-23 17:52

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0004_alter_categories_slug"),
    ]

    operations = [
        migrations.AlterField(
            model_name="categories",
            name="slug",
            field=models.SlugField(
                blank=True, max_length=32, unique=True, verbose_name="URL"
            ),
        ),
    ]
