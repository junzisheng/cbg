# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CrawlOrders',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('oid', models.CharField(blank=True, max_length=32)),
                ('uname', models.CharField(blank=True, max_length=32)),
                ('umobile', models.CharField(blank=True, max_length=64)),
                ('uemail', models.CharField(blank=True, max_length=12)),
                ('uaddress', models.CharField(blank=True, max_length=12)),
                ('memo', models.CharField(blank=True, max_length=25)),
                ('price', models.IntegerField(null=True, blank=True)),
                ('real_price', models.IntegerField(null=True, blank=True)),
                ('points', models.IntegerField(null=True, blank=True)),
                ('real_points', models.IntegerField(null=True, blank=True)),
                ('pay_status', models.CharField(blank=True, max_length=32)),
                ('pay_channel', models.CharField(blank=True, max_length=32)),
                ('pay_time', models.DateTimeField(null=True, blank=True)),
                ('pay_tradeno', models.CharField(blank=True, max_length=64)),
                ('user_ip', models.CharField(blank=True, max_length=64)),
                ('user_agent', models.CharField(blank=True, max_length=256)),
                ('createtime', models.DateTimeField(null=True, blank=True)),
                ('status', models.CharField(blank=True, max_length=16)),
                ('closing_time', models.DateTimeField(null=True, blank=True)),
                ('delete_falg', models.DateTimeField(null=True, blank=True)),
            ],
        ),
    ]
