# Generated by Django 4.1.3 on 2022-12-18 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0018_book_number_of_likes'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='number_of_reviews',
            field=models.IntegerField(default=0),
        ),
    ]
