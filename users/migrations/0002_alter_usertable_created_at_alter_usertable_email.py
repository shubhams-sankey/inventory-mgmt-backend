# Generated by Django 5.0.6 on 2024-06-14 09:37

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usertable',
            name='created_at',
            field=models.DateField(default=datetime.datetime(2024, 6, 14, 9, 37, 9, 548944)),
        ),
        migrations.AlterField(
            model_name='usertable',
            name='email',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
