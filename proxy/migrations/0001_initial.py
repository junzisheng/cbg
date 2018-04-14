# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Proxys',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('ip', models.CharField(max_length=11, blank=True)),
                ('port', models.SmallIntegerField()),
                ('types', models.SmallIntegerField()),
                ('protocol', models.SmallIntegerField()),
                ('country', models.CharField(max_length=32)),
                ('area', models.CharField(max_length=32)),
                ('updatetime', models.DateTimeField(auto_now_add=True)),
                ('speed', models.DecimalField(max_digits=5, decimal_places=2)),
                ('score', models.SmallIntegerField()),
            ],
        ),
    ]
