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
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('nickname', models.CharField(blank=True, max_length=32)),
                ('sex', models.CharField(blank=True, max_length=10)),
                ('age', models.CharField(blank=True, max_length=20)),
                ('head_image', models.CharField(blank=True, max_length=100)),
                ('v', models.CharField(blank=True, max_length=16)),
                ('introduce', models.CharField(blank=True, max_length=600)),
                ('alias', models.CharField(blank=True, max_length=60)),
                ('attr', models.CharField(blank=True, max_length=128)),
                ('comment_limit', models.DateTimeField(blank=True, null=True)),
                ('points', models.IntegerField(default=0, blank=True, null=True)),
                ('auto_country', models.CharField(blank=True, max_length=32)),
                ('auto_province', models.CharField(blank=True, max_length=32)),
                ('auto_city', models.CharField(blank=True, max_length=32)),
                ('auto_district', models.CharField(blank=True, max_length=32)),
                ('be_used_points', models.IntegerField(default=0, blank=True, null=True)),
                ('currency', models.IntegerField(default=0, blank=True, null=True)),
                ('give_currency', models.IntegerField(default=0, blank=True, null=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'user_profile',
            },
        ),
    ]
