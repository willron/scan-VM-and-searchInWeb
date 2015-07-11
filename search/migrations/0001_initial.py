# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='VMServer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
                ('ip', models.CharField(max_length=30)),
                ('mac', models.CharField(max_length=30)),
                ('hostserverip', models.CharField(max_length=30)),
                ('os', models.CharField(max_length=30)),
            ],
        ),
    ]
