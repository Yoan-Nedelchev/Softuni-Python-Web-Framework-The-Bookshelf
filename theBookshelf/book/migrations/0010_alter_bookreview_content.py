# Generated by Django 4.1.3 on 2022-12-10 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0009_bookreview'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookreview',
            name='content',
            field=models.TextField(blank=True, null=True),
        ),
    ]
