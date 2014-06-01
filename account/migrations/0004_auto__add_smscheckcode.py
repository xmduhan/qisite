# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'smsCheckCode'
        db.create_table(u'account_smscheckcode', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('checkCode', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('createTime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 6, 1, 0, 0))),
        ))
        db.send_create_signal(u'account', ['smsCheckCode'])


    def backwards(self, orm):
        # Deleting model 'smsCheckCode'
        db.delete_table(u'account_smscheckcode')


    models = {
        u'account.smscheckcode': {
            'Meta': {'object_name': 'smsCheckCode'},
            'checkCode': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'createTime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 6, 1, 0, 0)'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'account.user': {
            'Meta': {'ordering': "['name']", 'object_name': 'User'},
            'birthDate': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'createBy': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'userCreated'", 'null': 'True', 'to': u"orm['account.User']"}),
            'createTime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 6, 1, 0, 0)'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modifyBy': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'userModified'", 'null': 'True', 'to': u"orm['account.User']"}),
            'modifyTime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 6, 1, 0, 0)'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['account']