# Generated by Django 4.0 on 2021-12-25 10:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0005_alter_uuidtaggeditem_content_type_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='place',
            options={'ordering': ('-updated_on',), 'permissions': [('special_status', 'Can see all places')]},
        ),
    ]
