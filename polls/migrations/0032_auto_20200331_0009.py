# Generated by Django 3.0.2 on 2020-03-30 21:09

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0031_auto_20200330_0020'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plantdata',
            name='MeasurementTime',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 30, 21, 9, 49, 744495, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='plantdata',
            name='ServerTime',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 30, 21, 9, 49, 744495, tzinfo=utc)),
        ),
    ]
