# Generated by Django 3.2.11 on 2022-02-17 20:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_alter_profile_deleted_on'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='resume_list',
            field=models.JSONField(default=dict, editable=False),
        ),
    ]
