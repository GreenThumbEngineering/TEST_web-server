# Generated by Django 3.0.2 on 2020-02-01 13:32

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0007_auto_20191221_1550'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Book',
        ),
        migrations.RemoveField(
            model_name='plantdata',
            name='ColorTemp',
        ),
        migrations.RemoveField(
            model_name='plantdata',
            name='Lux',
        ),
        migrations.RemoveField(
            model_name='plantdata',
            name='Pressure',
        ),
        migrations.RemoveField(
            model_name='plantdata',
            name='RGB',
        ),
        migrations.RemoveField(
            model_name='plantdata',
            name='Soil',
        ),
        migrations.RemoveField(
            model_name='plantdata',
            name='Time',
        ),
        migrations.RemoveField(
            model_name='plantdata',
            name='deviceID',
        ),
        migrations.AddField(
            model_name='plantdata',
            name='DeviceID',
            field=models.CharField(default='', max_length=20),
        ),
        migrations.AddField(
            model_name='plantdata',
            name='Luminosity',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='plantdata',
            name='MeasurementTime',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name='plantdata',
            name='ServerTime',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name='plantdata',
            name='SoilMoisture',
            field=models.IntegerField(default=0),
        ),
    ]
