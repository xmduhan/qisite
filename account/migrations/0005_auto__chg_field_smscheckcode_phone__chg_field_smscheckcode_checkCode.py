# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'SmsCheckCode.phone'
        db.alter_column(u'account_smscheckcode', 'phone', self.gf('django.db.models.fields.CharField')(max_length=20))

        # Changing field 'SmsCheckCode.checkCode'
        db.alter_column(u'account_smscheckcode', 'checkCode', self.gf('django.db.models.fields.CharField')(max_length=20))

    def backwards(self, orm):

        # Changing field 'SmsCheckCode.phone'
        db.alter_column(u'account_smscheckcode', 'phone', self.gf('django.db.models.fields.CharField')(max_length=50))

        # Changing field 'SmsCheckCode.checkCode'
        db.alter_column(u'account_smscheckcode', 'checkCode', self.gf('django.db.models.fields.CharField')(max_length=50))

    models = {
        u'account.smscheckcode': {
            'Meta': {'ordering': "['createTime']", 'object_name': 'SmsCheckCode'},
            'checkCode': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'createTime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        u'account.user': {
            'Meta': {'ordering': "['name']", 'object_name': 'User'},
            'birthDate': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'createBy': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'userCreated'", 'null': 'True', 'to': u"orm['account.User']"}),
            'createTime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modifyBy': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'userModified'", 'null': 'True', 'to': u"orm['account.User']"}),
            'modifyTime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['account']