# Generated by Django 4.1.7 on 2023-03-14 09:29

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categories',
            name='description',
            field=models.CharField(blank=True, max_length=64, verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='categories',
            name='slug',
            field=models.SlugField(blank=True, max_length=32, unique=True, verbose_name='URL'),
        ),
        migrations.AlterField(
            model_name='categories',
            name='title',
            field=models.CharField(max_length=32, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='posts',
            name='image',
            field=models.ImageField(blank=True, upload_to='post_images/%y/%m/%d', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=('png', 'jpg', 'jpeg', 'gif', 'webp'))], verbose_name='Превью'),
        ),
        migrations.AlterField(
            model_name='posts',
            name='short_descrtiprion',
            field=models.CharField(blank=True, max_length=64, verbose_name='Короткое описание'),
        ),
        migrations.AlterField(
            model_name='posts',
            name='slug',
            field=models.SlugField(blank=True, max_length=32, unique=True, verbose_name='URL'),
        ),
        migrations.AlterField(
            model_name='posts',
            name='title',
            field=models.CharField(max_length=32, verbose_name='Заголовок'),
        ),
    ]
