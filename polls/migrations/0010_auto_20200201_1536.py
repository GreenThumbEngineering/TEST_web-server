# Generated by Django 3.0.2 on 2020-02-01 13:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0009_auto_20200201_1535'),
    ]

    operations = [
        migrations.RenameField(
            model_name='plantdata',
            old_name='EspID',
            new_name='deviceID',
        ),
    ]
