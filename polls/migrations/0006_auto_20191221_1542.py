# Generated by Django 2.2.7 on 2019-12-21 15:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0005_userprofileinfo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofileinfo',
            name='portfolio_site',
        ),
        migrations.RemoveField(
            model_name='userprofileinfo',
            name='profile_pic',
        ),
    ]
