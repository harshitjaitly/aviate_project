# Generated by Django 3.2.11 on 2022-02-17 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_profile_deleted_on'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='resume',
            field=models.FileField(default=None, upload_to='uploads/% Y/% m/% d/'),
        ),
    ]
