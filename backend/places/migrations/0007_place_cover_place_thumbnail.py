# Generated by Django 4.0 on 2021-12-28 08:25

from django.db import migrations, models
import places.utils


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0006_alter_place_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='place',
            name='cover',
            field=models.ImageField(blank=True, upload_to=places.utils.cover_image_path, verbose_name='Cover photo'),
        ),
        migrations.AddField(
            model_name='place',
            name='thumbnail',
            field=models.ImageField(null=True, upload_to=places.utils.cover_thumbnail_path),
        ),
    ]
