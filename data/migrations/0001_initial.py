# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'User'
        db.create_table('data_user', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('email', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('billing_zip', self.gf('django.db.models.fields.CharField')(max_length=11)),
            ('terms', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('last_access', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('data', ['User'])

        # Adding model 'Package'
        db.create_table('data_package', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('short_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('price', self.gf('django.db.models.fields.DecimalField')(max_digits=6, decimal_places=2)),
            ('prints', self.gf('django.db.models.fields.IntegerField')()),
            ('additional_price_per_print', self.gf('django.db.models.fields.DecimalField')(max_digits=6, decimal_places=2)),
            ('albums', self.gf('django.db.models.fields.IntegerField')()),
            ('slideshow', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('shipping', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('table_cards', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('guest_reminders', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('enabled', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('data', ['Package'])

        # Adding model 'Type'
        db.create_table('data_type', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('data', ['Type'])

        # Adding model 'Event'
        db.create_table('data_event', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['data.User'])),
            ('package', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['data.Package'])),
            ('start', self.gf('django.db.models.fields.DateTimeField')()),
            ('end', self.gf('django.db.models.fields.DateTimeField')()),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('pin', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('last_access', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('access_count', self.gf('django.db.models.fields.IntegerField')()),
            ('enabled', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('data', ['Event'])

        # Adding model 'Address'
        db.create_table('data_address', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['data.Event'])),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('lat', self.gf('django.db.models.fields.DecimalField')(max_digits=9, decimal_places=6)),
            ('lng', self.gf('django.db.models.fields.DecimalField')(max_digits=9, decimal_places=6)),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('data', ['Address'])

        # Adding model 'Guest'
        db.create_table('data_guest', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['data.Event'])),
            ('type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['data.Type'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('email', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('data', ['Guest'])

        # Adding model 'Photo'
        db.create_table('data_photo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['data.Event'])),
            ('guest', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['data.Guest'])),
            ('type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['data.Type'])),
            ('filename', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('caption', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('streamable', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('metrics', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('data', ['Photo'])

        # Adding model 'Album'
        db.create_table('data_album', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['data.Event'])),
            ('type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['data.Type'])),
            ('photo', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['data.Photo'], null=True, on_delete=models.SET_NULL)),
            ('short_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('data', ['Album'])

        # Adding model 'AlbumPhoto'
        db.create_table('data_albumphoto', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('album', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['data.Album'])),
            ('photo', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['data.Photo'])),
        ))
        db.send_create_signal('data', ['AlbumPhoto'])


    def backwards(self, orm):
        # Deleting model 'User'
        db.delete_table('data_user')

        # Deleting model 'Package'
        db.delete_table('data_package')

        # Deleting model 'Type'
        db.delete_table('data_type')

        # Deleting model 'Event'
        db.delete_table('data_event')

        # Deleting model 'Address'
        db.delete_table('data_address')

        # Deleting model 'Guest'
        db.delete_table('data_guest')

        # Deleting model 'Photo'
        db.delete_table('data_photo')

        # Deleting model 'Album'
        db.delete_table('data_album')

        # Deleting model 'AlbumPhoto'
        db.delete_table('data_albumphoto')


    models = {
        'data.address': {
            'Meta': {'object_name': 'Address'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.Event']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lat': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '6'}),
            'lng': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '6'})
        },
        'data.album': {
            'Meta': {'object_name': 'Album'},
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.Event']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'photo': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['data.Photo']", 'null': 'True', 'on_delete': 'models.SET_NULL'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.Type']"})
        },
        'data.albumphoto': {
            'Meta': {'object_name': 'AlbumPhoto'},
            'album': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.Album']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'photo': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.Photo']"})
        },
        'data.event': {
            'Meta': {'object_name': 'Event'},
            'access_count': ('django.db.models.fields.IntegerField', [], {}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'end': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_access': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'package': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.Package']"}),
            'pin': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'start': ('django.db.models.fields.DateTimeField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.User']"})
        },
        'data.guest': {
            'Meta': {'object_name': 'Guest'},
            'email': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.Event']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.Type']"})
        },
        'data.package': {
            'Meta': {'object_name': 'Package'},
            'additional_price_per_print': ('django.db.models.fields.DecimalField', [], {'max_digits': '6', 'decimal_places': '2'}),
            'albums': ('django.db.models.fields.IntegerField', [], {}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'guest_reminders': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'price': ('django.db.models.fields.DecimalField', [], {'max_digits': '6', 'decimal_places': '2'}),
            'prints': ('django.db.models.fields.IntegerField', [], {}),
            'shipping': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slideshow': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'table_cards': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'data.photo': {
            'Meta': {'object_name': 'Photo'},
            'caption': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.Event']"}),
            'filename': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'guest': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.Guest']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'metrics': ('django.db.models.fields.TextField', [], {}),
            'streamable': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.Type']"})
        },
        'data.type': {
            'Meta': {'object_name': 'Type'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'data.user': {
            'Meta': {'object_name': 'User'},
            'billing_zip': ('django.db.models.fields.CharField', [], {'max_length': '11'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_access': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'terms': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['data']