# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Paper.description1'
        db.add_column(u'home_paper', 'description1',
                      self.gf('django.db.models.fields.CharField')(default='hello', max_length=1000),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Paper.description1'
        db.delete_column(u'home_paper', 'description1')


    models = {
        u'home.catalog': {
            'Meta': {'object_name': 'Catalog'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'create_date': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modify_date': ('django.db.models.fields.DateTimeField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'ord': ('django.db.models.fields.IntegerField', [], {}),
            'papers': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['home.Paper']", 'through': u"orm['home.CatalogPaper']", 'symmetrical': 'False'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Catalog']", 'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '5'})
        },
        u'home.catalogpaper': {
            'Meta': {'ordering': "['ord']", 'object_name': 'CatalogPaper'},
            'catalog': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Catalog']"}),
            'create_date': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modify_date': ('django.db.models.fields.DateTimeField', [], {}),
            'ord': ('django.db.models.fields.IntegerField', [], {}),
            'paper': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Paper']"}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '5'})
        },
        u'home.choice': {
            'Meta': {'ordering': "['ord']", 'object_name': 'Choice'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'create_date': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modify_date': ('django.db.models.fields.DateTimeField', [], {}),
            'ord': ('django.db.models.fields.IntegerField', [], {}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Question']"}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.ChoiceType']"})
        },
        u'home.choicetype': {
            'Meta': {'ordering': "['ord']", 'object_name': 'ChoiceType'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'create_date': ('django.db.models.fields.DateTimeField', [], {}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modify_date': ('django.db.models.fields.DateTimeField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'ord': ('django.db.models.fields.IntegerField', [], {}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '5'})
        },
        u'home.paper': {
            'Meta': {'ordering': "['name']", 'object_name': 'Paper'},
            'create_date': ('django.db.models.fields.DateTimeField', [], {}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'description1': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modify_date': ('django.db.models.fields.DateTimeField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '5'})
        },
        u'home.question': {
            'Meta': {'ordering': "['ord']", 'object_name': 'Question'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'create_date': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modify_date': ('django.db.models.fields.DateTimeField', [], {}),
            'ord': ('django.db.models.fields.IntegerField', [], {}),
            'paper': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Paper']"}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.QuestionType']"})
        },
        u'home.questiontype': {
            'Meta': {'ordering': "['ord']", 'object_name': 'QuestionType'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'create_date': ('django.db.models.fields.DateTimeField', [], {}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modify_date': ('django.db.models.fields.DateTimeField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'ord': ('django.db.models.fields.IntegerField', [], {}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '5'})
        },
        u'home.user': {
            'Meta': {'ordering': "['phone']", 'object_name': 'User'},
            'create_date': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modify_date': ('django.db.models.fields.DateTimeField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '5'})
        },
        u'home.userchoice': {
            'Meta': {'object_name': 'UserChoice'},
            'choice': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Choice']"}),
            'create_date': ('django.db.models.fields.DateTimeField', [], {}),
            'grade': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modify_date': ('django.db.models.fields.DateTimeField', [], {}),
            'ord': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'userquestion': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.UserQuestion']"})
        },
        u'home.userpaper': {
            'Meta': {'object_name': 'UserPaper'},
            'create_date': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modify_date': ('django.db.models.fields.DateTimeField', [], {}),
            'paper': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Paper']"}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.User']"})
        },
        u'home.userquestion': {
            'Meta': {'object_name': 'UserQuestion'},
            'create_date': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modify_date': ('django.db.models.fields.DateTimeField', [], {}),
            'ord': ('django.db.models.fields.IntegerField', [], {}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Question']"}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'userpaper': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.UserPaper']"})
        }
    }

    complete_apps = ['home']