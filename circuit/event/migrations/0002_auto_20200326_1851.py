# Generated by Django 3.0.4 on 2020-03-26 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='city',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='event',
            name='country',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='event',
            name='partner_tag',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='event',
            name='partner_url',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='event',
            name='state',
            field=models.CharField(max_length=200),
        ),
    ]
