# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0003_last_login_allow_null'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='is_archived',
            field=models.BooleanField(default=False, help_text=b'If the photo is archived.'),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_login',
            field=models.DateTimeField(null=True, verbose_name='last login', blank=True),
        ),
    ]
