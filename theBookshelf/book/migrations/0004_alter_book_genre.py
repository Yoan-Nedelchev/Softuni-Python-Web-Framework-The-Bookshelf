# Generated by Django 4.1.3 on 2022-12-08 22:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0003_book_genre'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='genre',
            field=models.CharField(choices=[('Romance', 'Romance'), ('Mystery', 'Mystery'), ('Fantasy and Science Fiction', 'Fantasy and Science Fiction'), ('Thrillers and Horrors', 'Thrillers and Horrors'), ('Young Adult', 'Young Adult'), ('Self-help', 'Self-help'), ('Biography, Autobiography and Memoir', 'Biography, Autobiography and Memoir'), ('Esoteric', 'Esoteric')], max_length=35),
        ),
    ]
