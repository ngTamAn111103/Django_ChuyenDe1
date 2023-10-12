# Generated by Django 4.2.5 on 2023-10-09 07:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Categori",
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
                ("name", models.CharField(max_length=255, unique=True)),
                (
                    "parent",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="cate_chill",
                        to="blog.categori",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="User",
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
                ("username", models.CharField(max_length=255, unique=True)),
                ("password", models.CharField(max_length=255)),
                ("fullname", models.CharField(max_length=255)),
                (
                    "avatar",
                    models.ImageField(
                        default="/MyBlogProject/media/9-anh-dai-dien-trang-inkythuatso-03-15-27-03.jpg",
                        upload_to="",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "role",
                    models.IntegerField(
                        choices=[(0, "Người dùng"), (1, "Quản trị viên")], default=0
                    ),
                ),
                ("level", models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name="Post",
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
                ("title", models.CharField(max_length=255)),
                ("content", models.TextField()),
                ("thumbnail", models.ImageField(upload_to="")),
                (
                    "status",
                    models.IntegerField(
                        choices=[(0, "Public"), (1, "Pravited")], default=1
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("views", models.IntegerField()),
                ("likes", models.IntegerField()),
                ("comments", models.IntegerField()),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="author_post",
                        to="blog.user",
                    ),
                ),
                (
                    "categori",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="categori_post",
                        to="blog.categori",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Like",
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
                (
                    "like_status",
                    models.IntegerField(
                        choices=[(0, "Liked"), (1, "Unlike")], default=1
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "post",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="like_post",
                        to="blog.post",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="user_like",
                        to="blog.user",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Comment",
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
                ("content", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "post",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="comment_post",
                        to="blog.post",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="user_comment",
                        to="blog.user",
                    ),
                ),
            ],
        ),
    ]
