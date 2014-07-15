# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'ApiKey.permission_mask'
        db.add_column(u'api_apikey', 'permission_mask',
                      self.gf('django.db.models.fields.BigIntegerField')(default=3),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'ApiKey.permission_mask'
        db.delete_column(u'api_apikey', 'permission_mask')


    models = {
        'api.apiaccount': {
            'Meta': {'object_name': 'ApiAccount'},
            'company': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'api.apikey': {
            'Meta': {'object_name': 'ApiKey'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['api.ApiAccount']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'permission_mask': ('django.db.models.fields.BigIntegerField', [], {'default': '3'}),
            'secret': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'version': ('django.db.models.fields.CharField', [], {'max_length': '25'})
        }
    }

    complete_apps = ['api']