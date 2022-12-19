# Generated by Django 4.1.3 on 2022-12-10 20:49

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('author', '0002_alter_author_biography'),
        ('book', '0012_alter_book_options_alter_bookreview_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='author',
            field=models.ForeignKey(default="1", on_delete=django.db.models.deletion.CASCADE, to='author.author'),
            preserve_default=False,
        ),
    ]