# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('nickname', models.CharField(max_length=32, blank=True)),
                ('sex', models.CharField(max_length=10, blank=True)),
                ('age', models.CharField(max_length=20, blank=True)),
                ('head_image', models.CharField(max_length=100, blank=True)),
                ('v', models.CharField(max_length=16, blank=True)),
                ('introduce', models.CharField(max_length=600, blank=True)),
                ('alias', models.CharField(max_length=60, blank=True)),
                ('attr', models.CharField(max_length=128, blank=True)),
                ('comment_limit', models.DateTimeField(null=True, blank=True)),
                ('points', models.IntegerField(default=0, null=True, blank=True)),
                ('auto_country', models.CharField(max_length=32, blank=True)),
                ('auto_province', models.CharField(max_length=32, blank=True)),
                ('auto_city', models.CharField(max_length=32, blank=True)),
                ('auto_district', models.CharField(max_length=32, blank=True)),
                ('be_used_points', models.IntegerField(default=0, null=True, blank=True)),
                ('currency', models.IntegerField(default=0, null=True, blank=True)),
                ('give_currency', models.IntegerField(default=0, null=True, blank=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'user_profile',
            },
        ),
    ]
