# Generated by Django 3.0.2 on 2020-02-01 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0008_auto_20200201_1532'),
    ]

    operations = [
        migrations.RenameField(
            model_name='plantdata',
            old_name='DeviceID',
            new_name='EspID',
        ),
        migrations.AddField(
            model_name='plantdata',
            name='RaspID',
            field=models.CharField(default='', max_length=20),
        ),
    ]
