# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Paper'
        db.create_table(u'survey_paper', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('inOrder', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('lookBack', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('style', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('createBy', self.gf('django.db.models.fields.related.ForeignKey')(related_name='paperCreated', to=orm['account.User'])),
            ('modifyBy', self.gf('django.db.models.fields.related.ForeignKey')(related_name='paperModified', to=orm['account.User'])),
            ('createTime', self.gf('django.db.models.fields.DateTimeField')()),
            ('modifyTime', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'survey', ['Paper'])

        # Adding model 'PaperCatalog'
        db.create_table(u'survey_papercatalog', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['survey.PaperCatalog'], null=True, blank=True)),
            ('ord', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'survey', ['PaperCatalog'])

        # Adding model 'Question'
        db.create_table(u'survey_question', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('contentLengh', self.gf('django.db.models.fields.IntegerField')()),
            ('valueMin', self.gf('django.db.models.fields.FloatField')()),
            ('valueMax', self.gf('django.db.models.fields.FloatField')()),
            ('stem', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['survey.Stem'])),
            ('confused', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('nextQuestion', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['survey.Question'])),
            ('paper', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['survey.Paper'])),
            ('createBy', self.gf('django.db.models.fields.related.ForeignKey')(related_name='questionCreated', to=orm['account.User'])),
            ('modifyBy', self.gf('django.db.models.fields.related.ForeignKey')(related_name='questionModified', to=orm['account.User'])),
            ('createTime', self.gf('django.db.models.fields.DateTimeField')()),
            ('modifyTime', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'survey', ['Question'])

        # Adding model 'QuestionCatalog'
        db.create_table(u'survey_questioncatalog', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['survey.QuestionCatalog'], null=True, blank=True)),
            ('ord', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'survey', ['QuestionCatalog'])

        # Adding model 'Stem'
        db.create_table(u'survey_stem', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('createBy', self.gf('django.db.models.fields.related.ForeignKey')(related_name='stemCreated', to=orm['account.User'])),
            ('modifyBy', self.gf('django.db.models.fields.related.ForeignKey')(related_name='stemModified', to=orm['account.User'])),
            ('createTime', self.gf('django.db.models.fields.DateTimeField')()),
            ('modifyTime', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'survey', ['Stem'])

        # Adding model 'Resource'
        db.create_table(u'survey_resource', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('resourceType', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('resourceUrl', self.gf('django.db.models.fields.CharField')(max_length=1000)),
            ('width', self.gf('django.db.models.fields.FloatField')()),
            ('height', self.gf('django.db.models.fields.FloatField')()),
            ('stem', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['survey.Stem'])),
            ('createBy', self.gf('django.db.models.fields.related.ForeignKey')(related_name='resourceCreated', to=orm['account.User'])),
            ('modifyBy', self.gf('django.db.models.fields.related.ForeignKey')(related_name='resourceModified', to=orm['account.User'])),
            ('createTime', self.gf('django.db.models.fields.DateTimeField')()),
            ('modifyTime', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'survey', ['Resource'])

        # Adding model 'Branch'
        db.create_table(u'survey_branch', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('ord', self.gf('django.db.models.fields.IntegerField')()),
            ('nextQuestion', self.gf('django.db.models.fields.related.ForeignKey')(related_name='fromBranch', to=orm['survey.Question'])),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['survey.Question'])),
            ('createBy', self.gf('django.db.models.fields.related.ForeignKey')(related_name='branchCreated', to=orm['account.User'])),
            ('modifyBy', self.gf('django.db.models.fields.related.ForeignKey')(related_name='branchModified', to=orm['account.User'])),
            ('createTime', self.gf('django.db.models.fields.DateTimeField')()),
            ('modifyTime', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'survey', ['Branch'])

        # Adding model 'Survey'
        db.create_table(u'survey_survey', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('paper', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['survey.Paper'])),
            ('targetOnly', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('shared', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('viewResult', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('resubmit', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('passwd', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('ipLimit', self.gf('django.db.models.fields.IntegerField')()),
            ('macLimit', self.gf('django.db.models.fields.IntegerField')()),
            ('publishTime', self.gf('django.db.models.fields.DateTimeField')()),
            ('endTime', self.gf('django.db.models.fields.DateTimeField')()),
            ('hardCost', self.gf('django.db.models.fields.FloatField')()),
            ('bonus', self.gf('django.db.models.fields.FloatField')()),
            ('fee', self.gf('django.db.models.fields.FloatField')()),
            ('validSampleLimit', self.gf('django.db.models.fields.IntegerField')()),
            ('createBy', self.gf('django.db.models.fields.related.ForeignKey')(related_name='surveyCreated', to=orm['account.User'])),
            ('modifyBy', self.gf('django.db.models.fields.related.ForeignKey')(related_name='surveyModified', to=orm['account.User'])),
            ('createTime', self.gf('django.db.models.fields.DateTimeField')()),
            ('modifyTime', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'survey', ['Survey'])

        # Adding model 'TargetCust'
        db.create_table(u'survey_targetcust', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('email', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('token', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('survey', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['survey.Survey'])),
            ('createBy', self.gf('django.db.models.fields.related.ForeignKey')(related_name='targetCustCreated', to=orm['account.User'])),
            ('modifyBy', self.gf('django.db.models.fields.related.ForeignKey')(related_name='targetCustModified', to=orm['account.User'])),
            ('createTime', self.gf('django.db.models.fields.DateTimeField')()),
            ('modifyTime', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'survey', ['TargetCust'])

        # Adding model 'Sample'
        db.create_table(u'survey_sample', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('targetCust', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['survey.TargetCust'], unique=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['account.User'])),
            ('ipAddress', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('macAddress', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('finished', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('isValid', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('paper', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['survey.Paper'])),
            ('createBy', self.gf('django.db.models.fields.related.ForeignKey')(related_name='sampleCreated', to=orm['account.User'])),
            ('modifyBy', self.gf('django.db.models.fields.related.ForeignKey')(related_name='sampleModified', to=orm['account.User'])),
            ('createTime', self.gf('django.db.models.fields.DateTimeField')()),
            ('modifyTime', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'survey', ['Sample'])

        # Adding model 'SampleItem'
        db.create_table(u'survey_sampleitem', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['survey.Question'])),
            ('content', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('score', self.gf('django.db.models.fields.FloatField')()),
            ('sample', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['survey.Sample'])),
            ('createBy', self.gf('django.db.models.fields.related.ForeignKey')(related_name='sampleItemCreated', to=orm['account.User'])),
            ('modifyBy', self.gf('django.db.models.fields.related.ForeignKey')(related_name='sampleItemModified', to=orm['account.User'])),
            ('createTime', self.gf('django.db.models.fields.DateTimeField')()),
            ('modifyTime', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'survey', ['SampleItem'])

        # Adding model 'CustList'
        db.create_table(u'survey_custlist', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('descrition', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('createBy', self.gf('django.db.models.fields.related.ForeignKey')(related_name='custListCreated', to=orm['account.User'])),
            ('modifyBy', self.gf('django.db.models.fields.related.ForeignKey')(related_name='custListModified', to=orm['account.User'])),
            ('createTime', self.gf('django.db.models.fields.DateTimeField')()),
            ('modifyTime', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'survey', ['CustList'])

        # Adding model 'CustListItem'
        db.create_table(u'survey_custlistitem', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('email', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('createBy', self.gf('django.db.models.fields.related.ForeignKey')(related_name='custListItemCreated', to=orm['account.User'])),
            ('modifyBy', self.gf('django.db.models.fields.related.ForeignKey')(related_name='custListItemModified', to=orm['account.User'])),
            ('createTime', self.gf('django.db.models.fields.DateTimeField')()),
            ('modifyTime', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'survey', ['CustListItem'])

        # Adding model 'DefineInfo'
        db.create_table(u'survey_defineinfo', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('ord', self.gf('django.db.models.fields.IntegerField')()),
            ('targetCust', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['survey.TargetCust'])),
            ('custListItem', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['survey.CustListItem'])),
            ('createBy', self.gf('django.db.models.fields.related.ForeignKey')(related_name='defineInfoCreated', to=orm['account.User'])),
            ('modifyBy', self.gf('django.db.models.fields.related.ForeignKey')(related_name='defineInfoModified', to=orm['account.User'])),
            ('createTime', self.gf('django.db.models.fields.DateTimeField')()),
            ('modifyTime', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'survey', ['DefineInfo'])


    def backwards(self, orm):
        # Deleting model 'Paper'
        db.delete_table(u'survey_paper')

        # Deleting model 'PaperCatalog'
        db.delete_table(u'survey_papercatalog')

        # Deleting model 'Question'
        db.delete_table(u'survey_question')

        # Deleting model 'QuestionCatalog'
        db.delete_table(u'survey_questioncatalog')

        # Deleting model 'Stem'
        db.delete_table(u'survey_stem')

        # Deleting model 'Resource'
        db.delete_table(u'survey_resource')

        # Deleting model 'Branch'
        db.delete_table(u'survey_branch')

        # Deleting model 'Survey'
        db.delete_table(u'survey_survey')

        # Deleting model 'TargetCust'
        db.delete_table(u'survey_targetcust')

        # Deleting model 'Sample'
        db.delete_table(u'survey_sample')

        # Deleting model 'SampleItem'
        db.delete_table(u'survey_sampleitem')

        # Deleting model 'CustList'
        db.delete_table(u'survey_custlist')

        # Deleting model 'CustListItem'
        db.delete_table(u'survey_custlistitem')

        # Deleting model 'DefineInfo'
        db.delete_table(u'survey_defineinfo')


    models = {
        u'account.user': {
            'Meta': {'ordering': "['name']", 'object_name': 'User'},
            'birthDate': ('django.db.models.fields.DateTimeField', [], {}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'createBy': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'userCreated'", 'null': 'True', 'to': u"orm['account.User']"}),
            'createTime': ('django.db.models.fields.DateTimeField', [], {}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modifyBy': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'userModified'", 'null': 'True', 'to': u"orm['account.User']"}),
            'modifyTime': ('django.db.models.fields.DateTimeField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'survey.branch': {
            'Meta': {'object_name': 'Branch'},
            'createBy': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'branchCreated'", 'to': u"orm['account.User']"}),
            'createTime': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modifyBy': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'branchModified'", 'to': u"orm['account.User']"}),
            'modifyTime': ('django.db.models.fields.DateTimeField', [], {}),
            'nextQuestion': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'fromBranch'", 'to': u"orm['survey.Question']"}),
            'ord': ('django.db.models.fields.IntegerField', [], {}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['survey.Question']"}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'survey.custlist': {
            'Meta': {'object_name': 'CustList'},
            'createBy': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'custListCreated'", 'to': u"orm['account.User']"}),
            'createTime': ('django.db.models.fields.DateTimeField', [], {}),
            'descrition': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modifyBy': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'custListModified'", 'to': u"orm['account.User']"}),
            'modifyTime': ('django.db.models.fields.DateTimeField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'survey.custlistitem': {
            'Meta': {'object_name': 'CustListItem'},
            'createBy': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'custListItemCreated'", 'to': u"orm['account.User']"}),
            'createTime': ('django.db.models.fields.DateTimeField', [], {}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modifyBy': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'custListItemModified'", 'to': u"orm['account.User']"}),
            'modifyTime': ('django.db.models.fields.DateTimeField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'survey.defineinfo': {
            'Meta': {'object_name': 'DefineInfo'},
            'createBy': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'defineInfoCreated'", 'to': u"orm['account.User']"}),
            'createTime': ('django.db.models.fields.DateTimeField', [], {}),
            'custListItem': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['survey.CustListItem']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modifyBy': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'defineInfoModified'", 'to': u"orm['account.User']"}),
            'modifyTime': ('django.db.models.fields.DateTimeField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'ord': ('django.db.models.fields.IntegerField', [], {}),
            'targetCust': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['survey.TargetCust']"}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'survey.paper': {
            'Meta': {'object_name': 'Paper'},
            'createBy': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'paperCreated'", 'to': u"orm['account.User']"}),
            'createTime': ('django.db.models.fields.DateTimeField', [], {}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inOrder': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'lookBack': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'modifyBy': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'paperModified'", 'to': u"orm['account.User']"}),
            'modifyTime': ('django.db.models.fields.DateTimeField', [], {}),
            'style': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        u'survey.papercatalog': {
            'Meta': {'object_name': 'PaperCatalog'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'ord': ('django.db.models.fields.IntegerField', [], {}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['survey.PaperCatalog']", 'null': 'True', 'blank': 'True'})
        },
        u'survey.question': {
            'Meta': {'object_name': 'Question'},
            'confused': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'contentLengh': ('django.db.models.fields.IntegerField', [], {}),
            'createBy': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'questionCreated'", 'to': u"orm['account.User']"}),
            'createTime': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modifyBy': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'questionModified'", 'to': u"orm['account.User']"}),
            'modifyTime': ('django.db.models.fields.DateTimeField', [], {}),
            'nextQuestion': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['survey.Question']"}),
            'paper': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['survey.Paper']"}),
            'stem': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['survey.Stem']"}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'valueMax': ('django.db.models.fields.FloatField', [], {}),
            'valueMin': ('django.db.models.fields.FloatField', [], {})
        },
        u'survey.questioncatalog': {
            'Meta': {'object_name': 'QuestionCatalog'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'ord': ('django.db.models.fields.IntegerField', [], {}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['survey.QuestionCatalog']", 'null': 'True', 'blank': 'True'})
        },
        u'survey.resource': {
            'Meta': {'object_name': 'Resource'},
            'createBy': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'resourceCreated'", 'to': u"orm['account.User']"}),
            'createTime': ('django.db.models.fields.DateTimeField', [], {}),
            'height': ('django.db.models.fields.FloatField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modifyBy': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'resourceModified'", 'to': u"orm['account.User']"}),
            'modifyTime': ('django.db.models.fields.DateTimeField', [], {}),
            'resourceType': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'resourceUrl': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'stem': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['survey.Stem']"}),
            'width': ('django.db.models.fields.FloatField', [], {})
        },
        u'survey.sample': {
            'Meta': {'object_name': 'Sample'},
            'createBy': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sampleCreated'", 'to': u"orm['account.User']"}),
            'createTime': ('django.db.models.fields.DateTimeField', [], {}),
            'finished': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ipAddress': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'isValid': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'macAddress': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'modifyBy': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sampleModified'", 'to': u"orm['account.User']"}),
            'modifyTime': ('django.db.models.fields.DateTimeField', [], {}),
            'paper': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['survey.Paper']"}),
            'targetCust': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['survey.TargetCust']", 'unique': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['account.User']"})
        },
        u'survey.sampleitem': {
            'Meta': {'object_name': 'SampleItem'},
            'content': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'createBy': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sampleItemCreated'", 'to': u"orm['account.User']"}),
            'createTime': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modifyBy': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sampleItemModified'", 'to': u"orm['account.User']"}),
            'modifyTime': ('django.db.models.fields.DateTimeField', [], {}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['survey.Question']"}),
            'sample': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['survey.Sample']"}),
            'score': ('django.db.models.fields.FloatField', [], {})
        },
        u'survey.stem': {
            'Meta': {'object_name': 'Stem'},
            'createBy': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'stemCreated'", 'to': u"orm['account.User']"}),
            'createTime': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modifyBy': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'stemModified'", 'to': u"orm['account.User']"}),
            'modifyTime': ('django.db.models.fields.DateTimeField', [], {}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '300'})
        },
        u'survey.survey': {
            'Meta': {'object_name': 'Survey'},
            'bonus': ('django.db.models.fields.FloatField', [], {}),
            'createBy': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'surveyCreated'", 'to': u"orm['account.User']"}),
            'createTime': ('django.db.models.fields.DateTimeField', [], {}),
            'endTime': ('django.db.models.fields.DateTimeField', [], {}),
            'fee': ('django.db.models.fields.FloatField', [], {}),
            'hardCost': ('django.db.models.fields.FloatField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ipLimit': ('django.db.models.fields.IntegerField', [], {}),
            'macLimit': ('django.db.models.fields.IntegerField', [], {}),
            'modifyBy': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'surveyModified'", 'to': u"orm['account.User']"}),
            'modifyTime': ('django.db.models.fields.DateTimeField', [], {}),
            'paper': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['survey.Paper']"}),
            'passwd': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'publishTime': ('django.db.models.fields.DateTimeField', [], {}),
            'resubmit': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'shared': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'targetOnly': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'validSampleLimit': ('django.db.models.fields.IntegerField', [], {}),
            'viewResult': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'survey.targetcust': {
            'Meta': {'object_name': 'TargetCust'},
            'createBy': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'targetCustCreated'", 'to': u"orm['account.User']"}),
            'createTime': ('django.db.models.fields.DateTimeField', [], {}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modifyBy': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'targetCustModified'", 'to': u"orm['account.User']"}),
            'modifyTime': ('django.db.models.fields.DateTimeField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'survey': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['survey.Survey']"}),
            'token': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['survey']