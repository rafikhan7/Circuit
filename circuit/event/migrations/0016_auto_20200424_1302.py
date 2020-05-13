# Generated by Django 2.2 on 2020-04-24 13:02

import django.contrib.gis.db.models.fields
from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0015_auto_20200424_1214'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='event',
            managers=[
                ('geo_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.RemoveField(
            model_name='event',
            name='position',
        ),
        migrations.AddField(
            model_name='event',
            name='geo_location',
            field=django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=4326),
        ),
    ]
