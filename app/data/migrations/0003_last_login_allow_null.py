# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

        dependencies = [
            ('data', '0002_auto_20151227_0723'),
        ]

        operations = [
            migrations.AlterField(
                model_name='user',
                name='last_login',
                field=models.DateTimeField(null=True),
            )
        ]
