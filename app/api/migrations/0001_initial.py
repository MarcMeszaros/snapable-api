# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import bitfield.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ApiAccount',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.EmailField(help_text=b'The email contact for the API.', max_length=75)),
                ('company', models.CharField(help_text=b'The name of the organization or company.', max_length=255, null=True)),
                ('created_at', models.DateTimeField(help_text=b'When the api account was created. (UTC)', auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ApiKey',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key', models.CharField(help_text=b'The API key.', unique=True, max_length=255, db_index=True)),
                ('secret', models.CharField(help_text=b'The API key secret.', max_length=255)),
                ('version', models.CharField(help_text=b'The API version that the key has access to.', max_length=25, choices=[(b'partner_v1', b'Partner (v1)'), (b'private_v1', b'Private (v1)')])),
                ('created_at', models.DateTimeField(help_text=b'When the API key was created. (UTC)', auto_now_add=True)),
                ('is_enabled', models.BooleanField(default=True, help_text=b'If the API key is enabled.')),
                ('permission_mask', bitfield.models.BitField(((b'create', b'Create'), (b'read', b'Read'), (b'update', b'Update'), (b'delete', b'Delete')), default=15, help_text=b'What permissions this API key has on data in the system.')),
                ('account', models.ForeignKey(to='api.ApiAccount')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
