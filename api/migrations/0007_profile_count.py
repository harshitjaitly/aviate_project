# Generated by Django 3.2.11 on 2022-02-17 19:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_profile_resume'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='count',
            field=models.IntegerField(default=0, editable=False),
        ),
    ]
