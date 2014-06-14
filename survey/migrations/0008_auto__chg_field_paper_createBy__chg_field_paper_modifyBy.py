# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Paper.createBy'
        db.alter_column(u'survey_paper', 'createBy_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['account.User']))

        # Changing field 'Paper.modifyBy'
        db.alter_column(u'survey_paper', 'modifyBy_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['account.User']))

    def backwards(self, orm):

        # Changing field 'Paper.createBy'
        db.alter_column(u'survey_paper', 'createBy_id', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['account.User']))

        # Changing field 'Paper.modifyBy'
        db.alter_column(u'survey_paper', 'modifyBy_id', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['account.User']))

    models = {
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
        },
        u'survey.branch': {
            'Meta': {'object_name': 'Branch'},
            'createBy': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'branchCreated_set'", 'to': u"orm['account.User']"}),
            'createTime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modifyBy': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'branchModified_set'", 'to': u"orm['account.User']"}),
            'modifyTime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'nextQuestion': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'fromBranch'", 'null': 'True', 'to': u"orm['survey.Question']"}),
            'ord': ('django.db.models.fields.IntegerField', [], {}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['survey.Question']"}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'survey.custlist': {
            'Meta': {'object_name': 'CustList'},
            'createBy': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'custListCreated_set'", 'to': u"orm['account.User']"}),
            'createTime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'descrition': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modifyBy': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'custListModified_set'", 'to': u"orm['account.User']"}),
            'modifyTime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'survey.custlistitem': {
            'Meta': {'object_name': 'CustListItem'},
            'createBy': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'custListItemCreated_set'", 'to': u"orm['account.User']"}),
            'createTime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'custList': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'custListItem_set'", 'to': u"orm['survey.CustList']"}),
            'defineInfo_set': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['survey.DefineInfo']", 'symmetrical': 'False'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modifyBy': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'custListItemModified_set'", 'to': u"orm['account.User']"}),
            'modifyTime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'survey.defineinfo': {
            'Meta': {'object_name': 'DefineInfo'},
            'createBy': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'defineInfoCreated_set'", 'to': u"orm['account.User']"}),
            'createTime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modifyBy': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'defineInfoModified_set'", 'to': u"orm['account.User']"}),
            'modifyTime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'ord': ('django.db.models.fields.IntegerField', [], {}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'survey.paper': {
            'Meta': {'ordering': "['title']", 'object_name': 'Paper'},
            'createBy': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'paperCreated_set'", 'null': 'True', 'to': u"orm['account.User']"}),
            'createTime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inOrder': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'lookBack': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'modifyBy': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'paperModified_set'", 'null': 'True', 'to': u"orm['account.User']"}),
            'modifyTime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'paging': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'questionNumStyle': ('django.db.models.fields.CharField', [], {'default': "'123'", 'max_length': '50'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        u'survey.papercatalog': {
            'Meta': {'object_name': 'PaperCatalog'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'createBy': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'paperCatalogCreated_set'", 'to': u"orm['account.User']"}),
            'createTime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modifyBy': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'paperCatalogModified_set'", 'to': u"orm['account.User']"}),
            'modifyTime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'ord': ('django.db.models.fields.IntegerField', [], {}),
            'paper_set': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['survey.Paper']", 'through': u"orm['survey.PaperCatalogPaper']", 'symmetrical': 'False'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['survey.PaperCatalog']", 'null': 'True', 'blank': 'True'})
        },
        u'survey.papercatalogpaper': {
            'Meta': {'object_name': 'PaperCatalogPaper'},
            'createBy': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'paperCatalogPaperCreated_set'", 'to': u"orm['account.User']"}),
            'createTime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modifyBy': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'paperCatalogPaperModified_set'", 'to': u"orm['account.User']"}),
            'modifyTime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'ord': ('django.db.models.fields.IntegerField', [], {}),
            'paper': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['survey.Paper']"}),
            'paperCatalog': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['survey.PaperCatalog']"})
        },
        u'survey.question': {
            'Meta': {'ordering': "['ord']", 'object_name': 'Question'},
            'branchNumStyle': ('django.db.models.fields.CharField', [], {'default': "'ABC'", 'max_length': '50'}),
            'confused': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'contentLength': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'createBy': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'questionCreated_set'", 'to': u"orm['account.User']"}),
            'createTime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modifyBy': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'questionModified_set'", 'to': u"orm['account.User']"}),
            'modifyTime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'nextQuestion': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['survey.Question']", 'null': 'True', 'blank': 'True'}),
            'ord': ('django.db.models.fields.IntegerField', [], {}),
            'paper': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['survey.Paper']", 'null': 'True', 'blank': 'True'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'valueMax': ('django.db.models.fields.FloatField', [], {'default': '10', 'null': 'True', 'blank': 'True'}),
            'valueMin': ('django.db.models.fields.FloatField', [], {'default': '0', 'null': 'True', 'blank': 'True'})
        },
        u'survey.questioncatalog': {
            'Meta': {'object_name': 'QuestionCatalog'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'createBy': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'questionCatalogCreated_set'", 'to': u"orm['account.User']"}),
            'createTime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modifyBy': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'questionCatalogModified_set'", 'to': u"orm['account.User']"}),
            'modifyTime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'ord': ('django.db.models.fields.IntegerField', [], {}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['survey.QuestionCatalog']", 'null': 'True', 'blank': 'True'}),
            'question_set': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['survey.Question']", 'through': u"orm['survey.QuestionCatalogQuestion']", 'symmetrical': 'False'})
        },
        u'survey.questioncatalogquestion': {
            'Meta': {'object_name': 'QuestionCatalogQuestion'},
            'createBy': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'questionCatalogQuestionCreated_set'", 'to': u"orm['account.User']"}),
            'createTime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modifyBy': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'questionCatalogQuestionModified_set'", 'to': u"orm['account.User']"}),
            'modifyTime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'ord': ('django.db.models.fields.IntegerField', [], {}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['survey.Question']"}),
            'questionCatalog': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['survey.QuestionCatalog']"})
        },
        u'survey.resource': {
            'Meta': {'object_name': 'Resource'},
            'createBy': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'resourceCreated_set'", 'to': u"orm['account.User']"}),
            'createTime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'height': ('django.db.models.fields.FloatField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modifyBy': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'resourceModified_set'", 'to': u"orm['account.User']"}),
            'modifyTime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['survey.Question']"}),
            'resourceType': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'resourceUrl': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'width': ('django.db.models.fields.FloatField', [], {})
        },
        u'survey.sample': {
            'Meta': {'object_name': 'Sample'},
            'createBy': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sampleCreated_set'", 'to': u"orm['account.User']"}),
            'createTime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'finished': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ipAddress': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'isValid': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'macAddress': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'modifyBy': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sampleModified_set'", 'to': u"orm['account.User']"}),
            'modifyTime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'paper': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['survey.Paper']"}),
            'targetCust': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['survey.TargetCust']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['account.User']", 'null': 'True', 'blank': 'True'})
        },
        u'survey.sampleitem': {
            'Meta': {'object_name': 'SampleItem'},
            'branch_set': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['survey.Branch']", 'symmetrical': 'False'}),
            'content': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'createBy': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sampleItemCreated_set'", 'to': u"orm['account.User']"}),
            'createTime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modifyBy': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sampleItemModified_set'", 'to': u"orm['account.User']"}),
            'modifyTime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['survey.Question']"}),
            'sample': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['survey.Sample']"}),
            'score': ('django.db.models.fields.FloatField', [], {'default': '0'})
        },
        u'survey.survey': {
            'Meta': {'object_name': 'Survey'},
            'bonus': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'createBy': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'surveyCreated_set'", 'to': u"orm['account.User']"}),
            'createTime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'endTime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'fee': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'hardCost': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ipLimit': ('django.db.models.fields.IntegerField', [], {'default': '5'}),
            'macLimit': ('django.db.models.fields.IntegerField', [], {'default': '5'}),
            'modifyBy': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'surveyModified_set'", 'to': u"orm['account.User']"}),
            'modifyTime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'paper': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['survey.Paper']"}),
            'passwd': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'publishTime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'resubmit': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'shared': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'targetOnly': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'validSampleLimit': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'viewResult': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        u'survey.targetcust': {
            'Meta': {'object_name': 'TargetCust'},
            'createBy': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'targetCustCreated_set'", 'to': u"orm['account.User']"}),
            'createTime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'defineInfo_set': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['survey.DefineInfo']", 'symmetrical': 'False'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modifyBy': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'targetCustModified_set'", 'to': u"orm['account.User']"}),
            'modifyTime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'survey': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'targetCust_set'", 'to': u"orm['survey.Survey']"}),
            'token': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['survey']