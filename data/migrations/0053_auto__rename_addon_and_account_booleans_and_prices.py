# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        db.rename_column(u'data_addon', 'price', 'amount')
        db.rename_column(u'data_addon', 'enabled', 'is_enabled')
        db.rename_column(u'data_accountuser', 'admin', 'is_admin')
        db.rename_column(u'data_accountaddon', 'paid', 'is_paid')
        db.rename_column(u'data_eventaddon', 'paid', 'is_paid')


    def backwards(self, orm):
        db.rename_column(u'data_addon', 'amount', 'price')
        db.rename_column(u'data_addon', 'is_enabled', 'enabled')
        db.rename_column(u'data_accountuser', 'is_admin', 'admin')
        db.rename_column(u'data_accountaddon', 'is_paid', 'paid')
        db.rename_column(u'data_eventaddon', 'is_paid', 'paid')


    models = {
        'api.apiaccount': {
            'Meta': {'object_name': 'ApiAccount'},
            'company': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'data.account': {
            'Meta': {'object_name': 'Account'},
            'addons': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['data.Addon']", 'through': "orm['data.AccountAddon']", 'symmetrical': 'False'}),
            'api_account': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['api.ApiAccount']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'package': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['data.Package']", 'null': 'True'}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['data.User']", 'through': "orm['data.AccountUser']", 'symmetrical': 'False'}),
            'valid_until': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True'})
        },
        'data.accountaddon': {
            'Meta': {'object_name': 'AccountAddon'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.Account']"}),
            'addon': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.Addon']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_paid': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'quantity': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        },
        'data.accountuser': {
            'Meta': {'object_name': 'AccountUser'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.Account']"}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_admin': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.User']"})
        },
        'data.addon': {
            'Meta': {'object_name': 'Addon'},
            'amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '6', 'decimal_places': '2'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'data.event': {
            'Meta': {'object_name': 'Event'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.Account']"}),
            'addons': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['data.Addon']", 'through': "orm['data.EventAddon']", 'symmetrical': 'False'}),
            'are_photos_streamable': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'are_photos_watermarked': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'cover': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'on_delete': 'models.SET_NULL', 'default': 'None', 'to': "orm['data.Photo']", 'blank': 'True', 'null': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'end_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.utcnow'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'pin': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'start_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.utcnow'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'tz_offset': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'url': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'uuid': ('uuidfield.fields.UUIDField', [], {'unique': 'True', 'max_length': '32', 'blank': 'True'})
        },
        'data.eventaddon': {
            'Meta': {'object_name': 'EventAddon'},
            'addon': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.Addon']"}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.Event']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_paid': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'quantity': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        },
        'data.guest': {
            'Meta': {'object_name': 'Guest'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.Event']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invited': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'data.location': {
            'Meta': {'object_name': 'Location'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.Event']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lat': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '9', 'decimal_places': '6'}),
            'lng': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '9', 'decimal_places': '6'})
        },
        'data.order': {
            'Meta': {'object_name': 'Order'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.Account']"}),
            'amount': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'amount_refunded': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'charge_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'coupon': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '255', 'null': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'items': ('jsonfield.fields.JSONField', [], {}),
            'paid': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.User']", 'null': 'True'})
        },
        'data.package': {
            'Meta': {'object_name': 'Package'},
            'amount': ('django.db.models.fields.IntegerField', [], {}),
            'enabled': ('django.db.models.fields.BooleanField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interval': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'interval_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'items': ('jsonfield.fields.JSONField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'trial_period_days': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'data.passwordnonce': {
            'Meta': {'object_name': 'PasswordNonce'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nonce': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.User']"}),
            'valid': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'data.photo': {
            'Meta': {'object_name': 'Photo'},
            'caption': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.Event']"}),
            'guest': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['data.Guest']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'streamable': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        'data.user': {
            'Meta': {'object_name': 'User'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'payment_gateway_user_id': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '255', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['data']