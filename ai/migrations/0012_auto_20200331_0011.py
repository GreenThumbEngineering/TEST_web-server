# Generated by Django 3.0.2 on 2020-03-30 21:11

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ai', '0011_auto_20200331_0009'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plantprediction',
            name='Timestamp',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 31, 0, 11, 36, 803245)),
        ),
    ]
