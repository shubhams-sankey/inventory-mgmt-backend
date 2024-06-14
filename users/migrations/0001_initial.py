# Generated by Django 5.0.6 on 2024-06-14 09:31

import datetime
import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserTable',
            fields=[
                ('userid', models.IntegerField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('firstname', models.CharField(max_length=255)),
                ('lastname', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=255, null=True)),
                ('email', models.CharField(max_length=50, unique=True)),
                ('phno', models.IntegerField(null=True)),
                ('pincode', models.IntegerField()),
                ('created_at', models.DateField(default=datetime.datetime(2024, 6, 14, 9, 31, 38, 406677))),
            ],
            options={
                'db_table': 'user_table',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='UserLoginTable',
            fields=[
                ('email', models.CharField(max_length=255, primary_key=True, serialize=False, unique=True)),
                ('password', models.CharField(max_length=255)),
                ('id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.usertable')),
            ],
            options={
                'db_table': 'user_login_table',
                'managed': True,
            },
        ),
    ]
