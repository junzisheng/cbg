# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SmsQueue',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('mobilephone', models.CharField(max_length=20)),
                ('msg', models.CharField(blank=True, max_length=200)),
                ('create_time', models.DateTimeField(blank=True, null=True)),
                ('deadline', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'sms_queue',
            },
        ),
    ]
