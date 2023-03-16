# Generated by Django 4.1.7 on 2023-03-16 18:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("blog", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="posts",
            name="author",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="author_posts",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Автор",
            ),
        ),
        migrations.AddField(
            model_name="posts",
            name="category",
            field=mptt.fields.TreeForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="posts",
                to="blog.categories",
                verbose_name="Категория",
            ),
        ),
        migrations.AddField(
            model_name="posts",
            name="likes",
            field=models.ManyToManyField(
                blank=True, default=0, related_name="likes", to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name="posts",
            name="updater",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="updated_posts",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Обновил",
            ),
        ),
        migrations.AddField(
            model_name="categories",
            name="parent",
            field=mptt.fields.TreeForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="children",
                to="blog.categories",
                verbose_name="Родительская категория",
            ),
        ),
        migrations.AddIndex(
            model_name="posts",
            index=models.Index(
                fields=["-fixed", "-created", "status"],
                name="blog_posts_fixed_d5f11c_idx",
            ),
        ),
    ]
