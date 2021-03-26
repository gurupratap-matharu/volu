# Generated by Django 3.1.6 on 2021-03-26 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0002_place_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='place',
            name='slug',
            field=models.SlugField(default='dummy', max_length=250, unique_for_date='created_on'),
            preserve_default=False,
        ),
    ]
