# Generated by Django 3.2.11 on 2022-02-19 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_alter_profile_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='password',
            field=models.CharField(blank=True, editable=False, max_length=255),
        ),
    ]