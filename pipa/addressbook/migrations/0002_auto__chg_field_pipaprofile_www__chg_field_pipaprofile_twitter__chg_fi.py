# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'PipaProfile.www'
        db.alter_column('addressbook_pipaprofile', 'www', self.gf('django.db.models.fields.URLField')(max_length=150, null=True))

        # Changing field 'PipaProfile.twitter'
        db.alter_column('addressbook_pipaprofile', 'twitter', self.gf('django.db.models.fields.URLField')(max_length=150, null=True))

        # Changing field 'PipaProfile.linkedin'
        db.alter_column('addressbook_pipaprofile', 'linkedin', self.gf('django.db.models.fields.URLField')(max_length=150, null=True))

        # Changing field 'PipaProfile.blog'
        db.alter_column('addressbook_pipaprofile', 'blog', self.gf('django.db.models.fields.URLField')(max_length=150, null=True))

        # Changing field 'PipaProfile.flickr'
        db.alter_column('addressbook_pipaprofile', 'flickr', self.gf('django.db.models.fields.URLField')(max_length=150, null=True))

        # Changing field 'PipaProfile.facebook'
        db.alter_column('addressbook_pipaprofile', 'facebook', self.gf('django.db.models.fields.URLField')(max_length=150, null=True))
    def backwards(self, orm):

        # Changing field 'PipaProfile.www'
        db.alter_column('addressbook_pipaprofile', 'www', self.gf('django.db.models.fields.CharField')(max_length=150, null=True))

        # Changing field 'PipaProfile.twitter'
        db.alter_column('addressbook_pipaprofile', 'twitter', self.gf('django.db.models.fields.CharField')(max_length=150, null=True))

        # Changing field 'PipaProfile.linkedin'
        db.alter_column('addressbook_pipaprofile', 'linkedin', self.gf('django.db.models.fields.CharField')(max_length=150, null=True))

        # Changing field 'PipaProfile.blog'
        db.alter_column('addressbook_pipaprofile', 'blog', self.gf('django.db.models.fields.CharField')(max_length=150, null=True))

        # Changing field 'PipaProfile.flickr'
        db.alter_column('addressbook_pipaprofile', 'flickr', self.gf('django.db.models.fields.CharField')(max_length=150, null=True))

        # Changing field 'PipaProfile.facebook'
        db.alter_column('addressbook_pipaprofile', 'facebook', self.gf('django.db.models.fields.CharField')(max_length=150, null=True))
    models = {
        'addressbook.pipaprofile': {
            'Meta': {'ordering': "('user__first_name',)", 'object_name': 'PipaProfile'},
            'blog': ('django.db.models.fields.URLField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '400', 'null': 'True', 'blank': 'True'}),
            'facebook': ('django.db.models.fields.URLField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'facebook_public': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'flickr': ('django.db.models.fields.URLField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'flickr_public': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'jabber': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'linkedin': ('django.db.models.fields.URLField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'linkedin_public': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'msn': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'public_name': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'show_profile': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'skype': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'sshpubkey': ('django.db.models.fields.TextField', [], {'max_length': '4000', 'null': 'True', 'blank': 'True'}),
            'sshpubkey_public': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'twitter': ('django.db.models.fields.URLField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'twitter_public': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'unique': 'True'}),
            'www': ('django.db.models.fields.URLField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'www_public': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'yahoo': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['addressbook']