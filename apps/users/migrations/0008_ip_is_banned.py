# Generated by Django 4.1.7 on 2023-04-02 14:03

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0007_ip_created_ip_updated"),
    ]

    operations = [
        migrations.AddField(
            model_name="ip",
            name="is_banned",
            field=models.BooleanField(default=False),
        ),
    ]