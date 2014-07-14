# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        db.rename_column(u'api_apiaccount', 'created', 'created_at')
        db.rename_column(u'api_apikey', 'created', 'created_at')
        db.rename_column(u'api_apikey', 'enabled', 'is_enabled')


    def backwards(self, orm):
        db.rename_column(u'api_apiaccount', 'created_at', 'created')
        db.rename_column(u'api_apikey', 'created_at', 'created')
        db.rename_column(u'api_apikey', 'is_enabled', 'enabled')


    models = {
        'api.apiaccount': {
            'Meta': {'object_name': 'ApiAccount'},
            'company': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'api.apikey': {
            'Meta': {'object_name': 'ApiKey'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['api.ApiAccount']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'permission_mask': ('django.db.models.fields.BigIntegerField', [], {'default': '3'}),
            'secret': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'version': ('django.db.models.fields.CharField', [], {'max_length': '25'})
        }
    }

    complete_apps = ['api']