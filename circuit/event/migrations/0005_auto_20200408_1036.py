# Generated by Django 3.0.4 on 2020-04-08 05:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0004_eventbookmark'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='eventbookmark',
            name='event_name',
        ),
        migrations.RemoveField(
            model_name='eventbookmark',
            name='event_type',
        ),
        migrations.RemoveField(
            model_name='eventbookmark',
            name='event_url',
        ),
    ]
