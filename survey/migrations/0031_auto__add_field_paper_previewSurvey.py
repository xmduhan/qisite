# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Paper.previewSurvey'
        db.add_column(u'survey_paper', 'previewSurvey',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='paperPreview_set', null=True, on_delete=models.SET_NULL, to=orm['survey.Survey']),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Paper.previewSurvey'
        db.delete_column(u'survey_paper', 'previewSurvey_id')


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
            'nextQuestion': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'fromBranch'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['survey.Question']"}),
            'ord': ('django.db.models.fields.IntegerField', [], {}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['survey.Question']"}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'survey.custlist': {
            'Meta': {'object_name': 'CustList'},
            'createBy': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'custListCreated_set'", 'to': u"orm['account.User']"}),
            'createTime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'descrition': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'null': 'True', 'blank': 'True'}),
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
            'defineInfo_set': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['survey.DefineInfo']", 'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
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
            'code': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'createBy': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'paperCreated_set'", 'null': 'True', 'to': u"orm['account.User']"}),
            'createTime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inOrder': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'lookBack': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'modifyBy': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'paperModified_set'", 'null': 'True', 'to': u"orm['account.User']"}),
            'modifyTime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'previewSurvey': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'paperPreview_set'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['survey.Survey']"}),
            'questionNumStyle': ('django.db.models.fields.CharField', [], {'default': "'123'", 'max_length': '50'}),
            'step': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'survey': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'paperReversed_set'", 'null': 'True', 'to': u"orm['survey.Survey']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'T'", 'max_length': '10'})
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
            'nextQuestion': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['survey.Question']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
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
            'finished': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ipAddress': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'isValid': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'modifyBy': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sampleModified_set'", 'to': u"orm['account.User']"}),
            'modifyTime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'nextQuestion': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['survey.Question']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'paper': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['survey.Paper']"}),
            'session': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'targetCust': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['survey.TargetCust']", 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['account.User']", 'null': 'True', 'blank': 'True'})
        },
        u'survey.sampleitem': {
            'Meta': {'object_name': 'SampleItem'},
            'branch_set': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['survey.Branch']", 'symmetrical': 'False'}),
            'content': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'createBy': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'sampleItemCreated_set'", 'null': 'True', 'to': u"orm['account.User']"}),
            'createTime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modifyBy': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'sampleItemModified_set'", 'null': 'True', 'to': u"orm['account.User']"}),
            'modifyTime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['survey.Question']"}),
            'sample': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['survey.Sample']"}),
            'score': ('django.db.models.fields.FloatField', [], {'default': '0'})
        },
        u'survey.survey': {
            'Meta': {'object_name': 'Survey'},
            'anonymous': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'bonus': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'code': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'createBy': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'surveyCreated_set'", 'to': u"orm['account.User']"}),
            'createTime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'custList': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['survey.CustList']", 'null': 'True', 'blank': 'True'}),
            'endTime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2016, 10, 13, 0, 0)'}),
            'fee': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'hardCost': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ipLimit': ('django.db.models.fields.IntegerField', [], {'default': '5'}),
            'lastSmsSendTime': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'macLimit': ('django.db.models.fields.IntegerField', [], {'default': '5'}),
            'modifyBy': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'surveyModified_set'", 'to': u"orm['account.User']"}),
            'modifyTime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'paper': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'survey_set'", 'null': 'True', 'to': u"orm['survey.Paper']"}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'paused': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'pay': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'publishTime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'resubmit': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'shared': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'A'", 'max_length': '5'}),
            'targetOnly': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'validSampleLimit': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'viewResult': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        u'survey.targetcust': {
            'Meta': {'object_name': 'TargetCust'},
            'createBy': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'targetCustCreated_set'", 'to': u"orm['account.User']"}),
            'createTime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'defineInfo_set': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['survey.DefineInfo']", 'null': 'True', 'blank': 'True'}),
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