# Generated by Django 3.0.8 on 2020-10-23 00:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CivicConnect', '0002_profile_dob'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='dob',
            field=models.DateField(blank=True, null=True),
        ),
    ]
