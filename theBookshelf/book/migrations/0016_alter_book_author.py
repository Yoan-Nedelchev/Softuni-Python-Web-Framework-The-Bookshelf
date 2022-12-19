# Generated by Django 4.1.3 on 2022-12-10 23:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('author', '0003_alter_author_genre'),
        ('book', '0015_alter_book_cover_photo_alter_book_genre_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='author',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='author.author'),
        ),
    ]