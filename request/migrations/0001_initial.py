# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CrawlData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('order_id', models.IntegerField()),
                ('server_name', models.CharField(max_length=32)),
                ('server_id', models.CharField(max_length=32)),
                ('area_name', models.CharField(max_length=32)),
                ('time_left', models.CharField(max_length=32)),
                ('price', models.CharField(max_length=16)),
                ('nickname', models.CharField(max_length=32)),
                ('collect_num', models.SmallIntegerField()),
                ('eid', models.CharField(max_length=64)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('dest_url', models.CharField(max_length=512)),
                ('crawl_time', models.DateTimeField(max_length=512)),
            ],
            options={
                'db_table': 'crawl_data',
            },
        ),
        migrations.CreateModel(
            name='CrawlOrders',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('createtime', models.DateTimeField(auto_created=True, null=True)),
                ('oid', models.CharField(blank=True, max_length=32)),
                ('uname', models.CharField(blank=True, max_length=32)),
                ('umobile', models.CharField(blank=True, max_length=64)),
                ('uemail', models.CharField(blank=True, max_length=12)),
                ('uaddress', models.CharField(blank=True, max_length=12)),
                ('memo', models.CharField(blank=True, max_length=25)),
                ('price', models.IntegerField(blank=True, null=True)),
                ('real_price', models.IntegerField(blank=True, null=True)),
                ('points', models.IntegerField(blank=True, null=True)),
                ('real_points', models.IntegerField(blank=True, null=True)),
                ('pay_status', models.CharField(blank=True, max_length=32)),
                ('pay_channel', models.CharField(blank=True, max_length=32)),
                ('pay_time', models.DateTimeField(blank=True, null=True)),
                ('pay_tradeno', models.CharField(blank=True, max_length=64)),
                ('user_ip', models.CharField(blank=True, max_length=64)),
                ('user_agent', models.CharField(blank=True, max_length=256)),
                ('status', models.CharField(blank=True, max_length=16)),
                ('closing_time', models.DateTimeField(blank=True, null=True)),
                ('delete_falg', models.DateTimeField(blank=True, null=True)),
            ],
        ),
    ]
