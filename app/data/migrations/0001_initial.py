# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import django.db.models.deletion
import jsonfield.fields
import django.utils.timezone
from django.conf import settings
import uuidfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('email', models.CharField(help_text=b"The user's email.", unique=True, max_length=255, db_index=True)),
                ('first_name', models.CharField(help_text=b"The user's first name.", max_length=255)),
                ('last_name', models.CharField(help_text=b"The user's last name.", max_length=255)),
                ('created_at', models.DateTimeField(help_text=b'When the user was created. (UTC)', auto_now_add=True)),
                ('payment_gateway_user_id', models.CharField(default=None, max_length=255, null=True, help_text=b'The user ID on the payment gateway linked to this user.', blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('valid_until', models.DateTimeField(default=None, help_text=b'If set, the account is valid until this date (UTC). [Usually set when buying a package.]', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AccountAddon',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('quantity', models.IntegerField(default=1, help_text=b'The quantity modifier of the addon.')),
                ('is_paid', models.BooleanField(default=False, help_text=b'If the event addon has been paid.')),
                ('account', models.ForeignKey(to='data.Account')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AccountUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_admin', models.BooleanField(default=False, help_text=b'If the user is an account admin.')),
                ('added_at', models.DateTimeField(help_text=b'When the user was added to the account. (UTC)', auto_now_add=True)),
                ('account', models.ForeignKey(to='data.Account')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Addon',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(help_text=b'The title of the addon.', max_length=255)),
                ('description', models.TextField(help_text=b'The addon description.')),
                ('amount', models.DecimalField(help_text=b'The per unit addon price.', max_digits=6, decimal_places=2)),
                ('is_enabled', models.BooleanField(default=True, help_text=b'If the addon is enabled or not.')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uuid', uuidfield.fields.UUIDField(help_text=b'A unique identifier for the event.', unique=True, max_length=32, editable=False, blank=True)),
                ('start_at', models.DateTimeField(default=datetime.datetime.utcnow, help_text=b'Event start time. (UTC)')),
                ('end_at', models.DateTimeField(default=datetime.datetime.utcnow, help_text=b'Event end time. (UTC)')),
                ('tz_offset', models.IntegerField(default=0, help_text=b'The timezone offset (in minutes) from UTC.')),
                ('title', models.CharField(help_text=b'Event title.', max_length=255)),
                ('url', models.CharField(help_text=b'A "short name" for the event.', unique=True, max_length=255)),
                ('is_public', models.BooleanField(default=True, help_text=b'Is the event considered "public".')),
                ('pin', models.CharField(help_text=b'Pseudo-random PIN used for private events.', max_length=255)),
                ('created_at', models.DateTimeField(help_text=b'When the event was created. (UTC)', auto_now_add=True)),
                ('is_enabled', models.BooleanField(default=True, help_text=b'Is the event considered "active" in the system.')),
                ('are_photos_streamable', models.BooleanField(default=True, help_text=b'Should the images be streamable by default when created.')),
                ('are_photos_watermarked', models.BooleanField(default=False, help_text=b'Should a watermark be applied to non-original images.')),
                ('account', models.ForeignKey(help_text=b'What account the event belongs to.', to='data.Account')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EventAddon',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('quantity', models.IntegerField(default=1, help_text=b'The quantity modifier of the addon.')),
                ('is_paid', models.BooleanField(default=False, help_text=b'If the event addon has been paid.')),
                ('addon', models.ForeignKey(to='data.Addon')),
                ('event', models.ForeignKey(to='data.Event')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Guest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text=b'The guest name.', max_length=255)),
                ('email', models.CharField(help_text=b'The guest email address.', max_length=255)),
                ('is_invited', models.BooleanField(default=False, help_text=b'If the guest has been invited.')),
                ('created_at', models.DateTimeField(help_text=b'The guest timestamp.', auto_now_add=True)),
                ('event', models.ForeignKey(to='data.Event')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('address', models.CharField(help_text=b'The location address.', max_length=255)),
                ('lat', models.DecimalField(default=0, help_text=b'The address latitude.', max_digits=9, decimal_places=6)),
                ('lng', models.DecimalField(default=0, help_text=b'The address longitude.', max_digits=9, decimal_places=6)),
                ('event', models.ForeignKey(help_text=b'The event this location belongs to.', to='data.Event')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount', models.IntegerField(default=0, help_text=b'The order amount. (USD cents)')),
                ('amount_refunded', models.IntegerField(default=0, help_text=b'The amount refunded. (USD cents)')),
                ('created_at', models.DateTimeField(help_text=b'When the order was processed. (UTC)', auto_now_add=True)),
                ('items', jsonfield.fields.JSONField(help_text=b'The items payed for.')),
                ('charge_id', models.CharField(help_text=b'The invoice id for the payment gateway.', max_length=255, null=True)),
                ('is_paid', models.BooleanField(default=False, help_text=b'If the order has been paid for.')),
                ('coupon', models.CharField(default=None, max_length=255, null=True, help_text=b'The coupon code used in the order.', choices=[(b'201bride', b'201bride -\xc2\xa2[1000]'), (b'adorii', b'adorii -\xc2\xa2[4900]'), (b'adorii5986', b'adorii5986 -\xc2\xa2[4900]'), (b'bespoke', b'bespoke -\xc2\xa2[1000]'), (b'betheman', b'betheman -\xc2\xa2[1000]'), (b'bridaldetective', b'bridaldetective -\xc2\xa2[1000]'), (b'budgetsavvy', b'budgetsavvy -\xc2\xa2[1000]'), (b'enfianced', b'enfianced -\xc2\xa2[1000]'), (b'gbg', b'gbg -\xc2\xa2[1000]'), (b'nonprofitedu', b'nonprofitedu -\xc2\xa2[4900]'), (b'poptastic', b'poptastic -\xc2\xa2[1000]'), (b'smartbride', b'smartbride -\xc2\xa2[1000]'), (b'snaptrial2013', b'snaptrial2013 -\xc2\xa2[4900]'), (b'snaptrial2014', b'snaptrial2014 -\xc2\xa2[4900]'), (b'weddingful5986', b'weddingful5986 -\xc2\xa2[4900]'), (b'wr2013', b'wr2013 -\xc2\xa2[1000]')])),
                ('account', models.ForeignKey(help_text=b'The account that the order is for.', to='data.Account')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, help_text=b'The user that made the order.', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Package',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('short_name', models.CharField(help_text=b'The package short name.', max_length=255)),
                ('name', models.CharField(help_text=b'The package long name.', max_length=255)),
                ('amount', models.IntegerField(help_text=b'The package price. (CENTS)')),
                ('is_enabled', models.BooleanField(default=True, help_text=b'If the package is enabled.')),
                ('items', jsonfield.fields.JSONField(help_text=b'The items included in the package.')),
                ('interval', models.CharField(default=None, choices=[(b'year', b'Year'), (b'month', b'Month'), (b'week', b'Week')], max_length=5, blank=True, help_text=b'The interval type for the package. (NULL/day/month/year)', null=True)),
                ('interval_count', models.IntegerField(default=0, help_text=b"The interval count for the package if the interval field isn't null.")),
                ('trial_period_days', models.IntegerField(default=0, help_text=b'How many days to offer a trial for.')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PasswordNonce',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nonce', models.CharField(help_text=b'The password nonce.', unique=True, max_length=255)),
                ('is_valid', models.BooleanField(default=True, help_text=b'If the nonce is still valid.')),
                ('created_at', models.DateTimeField(help_text=b'When the nonce was created. (UTC)', auto_now_add=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('caption', models.CharField(help_text=b'The photo caption.', max_length=255, blank=True)),
                ('is_streamable', models.BooleanField(default=True, help_text=b'If the photo is streamable.')),
                ('created_at', models.DateTimeField(help_text=b'The photo timestamp.', auto_now_add=True)),
                ('event', models.ForeignKey(help_text=b'The event the photo belongs to.', to='data.Event')),
                ('guest', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, default=None, blank=True, to='data.Guest', help_text=b'The guest who took the photo.', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='event',
            name='addons',
            field=models.ManyToManyField(to='data.Addon', through='data.EventAddon'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='cover',
            field=models.ForeignKey(related_name=b'+', on_delete=django.db.models.deletion.SET_NULL, default=None, blank=True, to='data.Photo', help_text=b'The image to use for the event cover.', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='accountaddon',
            name='addon',
            field=models.ForeignKey(to='data.Addon'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='account',
            name='addons',
            field=models.ManyToManyField(to='data.Addon', through='data.AccountAddon'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='account',
            name='api_account',
            field=models.ForeignKey(default=None, blank=True, to='api.ApiAccount', help_text=b'The API Account this account was created by. (None = Snapable)', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='account',
            name='package',
            field=models.ForeignKey(default=None, to='data.Package', help_text=b'The active package associated with the account.', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='account',
            name='users',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, through='data.AccountUser'),
            preserve_default=True,
        ),
    ]
