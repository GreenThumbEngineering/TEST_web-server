# Generated by Django 3.0.2 on 2020-02-04 19:08

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0021_auto_20200204_0042'),
    ]

    operations = [
        migrations.CreateModel(
            name='Water',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('MeasurementTime', models.DateTimeField(default=datetime.datetime.now)),
                ('WaterAdded', models.FloatField()),
                ('Plant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.Plants')),
            ],
        ),
        migrations.CreateModel(
            name='NDVIMeasurement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('MeasurementTime', models.DateTimeField(default=datetime.datetime.now)),
                ('NDVI_value', models.FloatField()),
                ('Plant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.Plants')),
            ],
        ),
    ]
