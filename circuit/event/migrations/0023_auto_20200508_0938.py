# Generated by Django 2.2 on 2020-05-08 09:38

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0022_auto_20200506_1327'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='latitude',
        ),
        migrations.RemoveField(
            model_name='event',
            name='longitude',
        ),
        migrations.AddField(
            model_name='event',
            name='address',
            field=models.CharField(default=-1.0, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='event',
            name='location',
            field=django.contrib.gis.db.models.fields.PointField("Location in Map", geography=True, blank=True, null=True,
        srid=4326, help_text="Point(longitude latitude)"),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='event',
            name='city',
            field=models.CharField(max_length=50),
        ),
    ]
