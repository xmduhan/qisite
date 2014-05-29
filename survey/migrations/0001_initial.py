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
            ('createTime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 5, 29, 0, 0))),
            ('modifyTime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 5, 29, 0, 0))),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('inOrder', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('questionNumStyle', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('lookBack', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('style', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('createBy', self.gf('django.db.models.fields.related.ForeignKey')(related_name='paperCreated_set', to=orm['account.User'])),
            ('modifyBy', self.gf('django.db.models.fields.related.ForeignKey')(related_name='paperModified_set', to=orm['account.User'])),
        ))
        db.send_create_signal(u'survey', ['Paper'])

        # Adding model 'PaperCatalog'
        db.create_table(u'survey_papercatalog', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('createTime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 5, 29, 0, 0))),
            ('modifyTime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 5, 29, 0, 0))),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['survey.PaperCatalog'], null=True, blank=True)),
            ('ord', self.gf('django.db.models.fields.IntegerField')()),
            ('createBy', self.gf('django.db.models.fields.related.ForeignKey')(related_name='paperCatalogCreated_set', to=orm['account.User'])),
            ('modifyBy', self.gf('django.db.models.fields.related.ForeignKey')(related_name='paperCatalogModified_set', to=orm['account.User'])),
        ))
        db.send_create_signal(u'survey', ['PaperCatalog'])

        # Adding model 'PaperCatalogPaper'
        db.create_table(u'survey_papercatalogpaper', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('createTime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 5, 29, 0, 0))),
            ('modifyTime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 5, 29, 0, 0))),
            ('paperCatalog', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['survey.PaperCatalog'])),
            ('paper', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['survey.Paper'])),
            ('ord', self.gf('django.db.models.fields.IntegerField')()),
            ('createBy', self.gf('django.db.models.fields.related.ForeignKey')(related_name='paperCatalogPaperCreated_set', to=orm['account.User'])),
            ('modifyBy', self.gf('django.db.models.fields.related.ForeignKey')(related_name='paperCatalogPaperModified_set', to=orm['account.User'])),
        ))
        db.send_create_signal(u'survey', ['PaperCatalogPaper'])

        # Adding model 'Question'
        db.create_table(u'survey_question', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('createTime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 5, 29, 0, 0))),
            ('modifyTime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 5, 29, 0, 0))),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('ord', self.gf('django.db.models.fields.IntegerField')()),
            ('contentLengh', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('valueMin', self.gf('django.db.models.fields.FloatField')(default=0, null=True, blank=True)),
            ('valueMax', self.gf('django.db.models.fields.FloatField')(default=10, null=True, blank=True)),
            ('confused', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('branchNumStyle', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('nextQuestion', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['survey.Question'], null=True, blank=True)),
            ('paper', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['survey.Paper'], null=True, blank=True)),
            ('createBy', self.gf('django.db.models.fields.related.ForeignKey')(related_name='questionCreated_set', to=orm['account.User'])),
            ('modifyBy', self.gf('django.db.models.fields.related.ForeignKey')(related_name='questionModified_set', to=orm['account.User'])),
        ))
        db.send_create_signal(u'survey', ['Question'])

        # Adding model 'QuestionCatalog'
        db.create_table(u'survey_questioncatalog', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('createTime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 5, 29, 0, 0))),
            ('modifyTime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 5, 29, 0, 0))),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['survey.QuestionCatalog'], null=True, blank=True)),
            ('ord', self.gf('django.db.models.fields.IntegerField')()),
            ('createBy', self.gf('django.db.models.fields.related.ForeignKey')(related_name='questionCatalogCreated_set', to=orm['account.User'])),
            ('modifyBy', self.gf('django.db.models.fields.related.ForeignKey')(related_name='questionCatalogModified_set', to=orm['account.User'])),
        ))
        db.send_create_signal(u'survey', ['QuestionCatalog'])

        # Adding model 'QuestionCatalogQuestion'
        db.create_table(u'survey_questioncatalogquestion', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('createTime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 5, 29, 0, 0))),
            ('modifyTime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 5, 29, 0, 0))),
            ('questionCatalog', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['survey.QuestionCatalog'])),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['survey.Question'])),
            ('ord', self.gf('django.db.models.fields.IntegerField')()),
            ('createBy', self.gf('django.db.models.fields.related.ForeignKey')(related_name='questionCatalogQuestionCreated_set', to=orm['account.User'])),
            ('modifyBy', self.gf('django.db.models.fields.related.ForeignKey')(related_name='questionCatalogQuestionModified_set', to=orm['account.User'])),
        ))
        db.send_create_signal(u'survey', ['QuestionCatalogQuestion'])

        # Adding model 'Stem'
        db.create_table(u'survey_stem', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('createTime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 5, 29, 0, 0))),
            ('modifyTime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 5, 29, 0, 0))),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['survey.Question'])),
            ('createBy', self.gf('django.db.models.fields.related.ForeignKey')(related_name='stemCreated_set', to=orm['account.User'])),
            ('modifyBy', self.gf('django.db.models.fields.related.ForeignKey')(related_name='stemModified_set', to=orm['account.User'])),
        ))
        db.send_create_signal(u'survey', ['Stem'])

        # Adding model 'Resource'
        db.create_table(u'survey_resource', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('createTime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 5, 29, 0, 0))),
            ('modifyTime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 5, 29, 0, 0))),
            ('resourceType', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('resourceUrl', self.gf('django.db.models.fields.CharField')(max_length=1000)),
            ('width', self.gf('django.db.models.fields.FloatField')()),
            ('height', self.gf('django.db.models.fields.FloatField')()),
            ('stem', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['survey.Stem'])),
            ('createBy', self.gf('django.db.models.fields.related.ForeignKey')(related_name='resourceCreated_set', to=orm['account.User'])),
            ('modifyBy', self.gf('django.db.models.fields.related.ForeignKey')(related_name='resourceModified_set', to=orm['account.User'])),
        ))
        db.send_create_signal(u'survey', ['Resource'])

        # Adding model 'Branch'
        db.create_table(u'survey_branch', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('createTime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 5, 29, 0, 0))),
            ('modifyTime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 5, 29, 0, 0))),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('ord', self.gf('django.db.models.fields.IntegerField')()),
            ('nextQuestion', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='fromBranch', null=True, to=orm['survey.Question'])),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['survey.Question'])),
            ('createBy', self.gf('django.db.models.fields.related.ForeignKey')(related_name='branchCreated_set', to=orm['account.User'])),
            ('modifyBy', self.gf('django.db.models.fields.related.ForeignKey')(related_name='branchModified_set', to=orm['account.User'])),
        ))
        db.send_create_signal(u'survey', ['Branch'])

        # Adding model 'Survey'
        db.create_table(u'survey_survey', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('createTime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 5, 29, 0, 0))),
            ('modifyTime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 5, 29, 0, 0))),
            ('paper', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['survey.Paper'])),
            ('targetOnly', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('shared', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('viewResult', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('resubmit', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('passwd', self.gf('django.db.models.fields.CharField')(max_length=10, blank=True)),
            ('ipLimit', self.gf('django.db.models.fields.IntegerField')(default=5)),
            ('macLimit', self.gf('django.db.models.fields.IntegerField')(default=5)),
            ('publishTime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 5, 29, 0, 0))),
            ('endTime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 5, 29, 0, 0))),
            ('hardCost', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('bonus', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('fee', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('validSampleLimit', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('createBy', self.gf('django.db.models.fields.related.ForeignKey')(related_name='surveyCreated_set', to=orm['account.User'])),
            ('modifyBy', self.gf('django.db.models.fields.related.ForeignKey')(related_name='surveyModified_set', to=orm['account.User'])),
        ))
        db.send_create_signal(u'survey', ['Survey'])

        # Adding model 'TargetCust'
        db.create_table(u'survey_targetcust', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('createTime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 5, 29, 0, 0))),
            ('modifyTime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 5, 29, 0, 0))),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('email', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('token', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('survey', self.gf('django.db.models.fields.related.ForeignKey')(related_name='targetCust_set', to=orm['survey.Survey'])),
            ('createBy', self.gf('django.db.models.fields.related.ForeignKey')(related_name='targetCustCreated_set', to=orm['account.User'])),
            ('modifyBy', self.gf('django.db.models.fields.related.ForeignKey')(related_name='targetCustModified_set', to=orm['account.User'])),
        ))
        db.send_create_signal(u'survey', ['TargetCust'])

        # Adding M2M table for field defineInfo_set on 'TargetCust'
        m2m_table_name = db.shorten_name(u'survey_targetcust_defineInfo_set')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('targetcust', models.ForeignKey(orm[u'survey.targetcust'], null=False)),
            ('defineinfo', models.ForeignKey(orm[u'survey.defineinfo'], null=False))
        ))
        db.create_unique(m2m_table_name, ['targetcust_id', 'defineinfo_id'])

        # Adding model 'Sample'
        db.create_table(u'survey_sample', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('createTime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 5, 29, 0, 0))),
            ('modifyTime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 5, 29, 0, 0))),
            ('targetCust', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['survey.TargetCust'], unique=True, null=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['account.User'], null=True, blank=True)),
            ('ipAddress', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('macAddress', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('finished', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('isValid', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('paper', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['survey.Paper'])),
            ('createBy', self.gf('django.db.models.fields.related.ForeignKey')(related_name='sampleCreated_set', to=orm['account.User'])),
            ('modifyBy', self.gf('django.db.models.fields.related.ForeignKey')(related_name='sampleModified_set', to=orm['account.User'])),
        ))
        db.send_create_signal(u'survey', ['Sample'])

        # Adding model 'SampleItem'
        db.create_table(u'survey_sampleitem', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('createTime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 5, 29, 0, 0))),
            ('modifyTime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 5, 29, 0, 0))),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['survey.Question'])),
            ('content', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('score', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('sample', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['survey.Sample'])),
            ('createBy', self.gf('django.db.models.fields.related.ForeignKey')(related_name='sampleItemCreated_set', to=orm['account.User'])),
            ('modifyBy', self.gf('django.db.models.fields.related.ForeignKey')(related_name='sampleItemModified_set', to=orm['account.User'])),
        ))
        db.send_create_signal(u'survey', ['SampleItem'])

        # Adding M2M table for field branch_set on 'SampleItem'
        m2m_table_name = db.shorten_name(u'survey_sampleitem_branch_set')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('sampleitem', models.ForeignKey(orm[u'survey.sampleitem'], null=False)),
            ('branch', models.ForeignKey(orm[u'survey.branch'], null=False))
        ))
        db.create_unique(m2m_table_name, ['sampleitem_id', 'branch_id'])

        # Adding model 'CustList'
        db.create_table(u'survey_custlist', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('createTime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 5, 29, 0, 0))),
            ('modifyTime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 5, 29, 0, 0))),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('descrition', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('createBy', self.gf('django.db.models.fields.related.ForeignKey')(related_name='custListCreated_set', to=orm['account.User'])),
            ('modifyBy', self.gf('django.db.models.fields.related.ForeignKey')(related_name='custListModified_set', to=orm['account.User'])),
        ))
        db.send_create_signal(u'survey', ['CustList'])

        # Adding model 'CustListItem'
        db.create_table(u'survey_custlistitem', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('createTime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 5, 29, 0, 0))),
            ('modifyTime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 5, 29, 0, 0))),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('email', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('custList', self.gf('django.db.models.fields.related.ForeignKey')(related_name='custListItem_set', to=orm['survey.CustList'])),
            ('createBy', self.gf('django.db.models.fields.related.ForeignKey')(related_name='custListItemCreated_set', to=orm['account.User'])),
            ('modifyBy', self.gf('django.db.models.fields.related.ForeignKey')(related_name='custListItemModified_set', to=orm['account.User'])),
        ))
        db.send_create_signal(u'survey', ['CustListItem'])

        # Adding M2M table for field defineInfo_set on 'CustListItem'
        m2m_table_name = db.shorten_name(u'survey_custlistitem_defineInfo_set')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('custlistitem', models.ForeignKey(orm[u'survey.custlistitem'], null=False)),
            ('defineinfo', models.ForeignKey(orm[u'survey.defineinfo'], null=False))
        ))
        db.create_unique(m2m_table_name, ['custlistitem_id', 'defineinfo_id'])

        # Adding model 'DefineInfo'
        db.create_table(u'survey_defineinfo', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('createTime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 5, 29, 0, 0))),
            ('modifyTime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 5, 29, 0, 0))),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('ord', self.gf('django.db.models.fields.IntegerField')()),
            ('createBy', self.gf('django.db.models.fields.related.ForeignKey')(related_name='defineInfoCreated_set', to=orm['account.User'])),
            ('modifyBy', self.gf('django.db.models.fields.related.ForeignKey')(related_name='defineInfoModified_set', to=orm['account.User'])),
        ))
        db.send_create_signal(u'survey', ['DefineInfo'])


    def backwards(self, orm):
        # Deleting model 'Paper'
        db.delete_table(u'survey_paper')

        # Deleting model 'PaperCatalog'
        db.delete_table(u'survey_papercatalog')

        # Deleting model 'PaperCatalogPaper'
        db.delete_table(u'survey_papercatalogpaper')

        # Deleting model 'Question'
        db.delete_table(u'survey_question')

        # Deleting model 'QuestionCatalog'
        db.delete_table(u'survey_questioncatalog')

        # Deleting model 'QuestionCatalogQuestion'
        db.delete_table(u'survey_questioncatalogquestion')

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

        # Removing M2M table for field defineInfo_set on 'TargetCust'
        db.delete_table(db.shorten_name(u'survey_targetcust_defineInfo_set'))

        # Deleting model 'Sample'
        db.delete_table(u'survey_sample')

        # Deleting model 'SampleItem'
        db.delete_table(u'survey_sampleitem')

        # Removing M2M table for field branch_set on 'SampleItem'
        db.delete_table(db.shorten_name(u'survey_sampleitem_branch_set'))

        # Deleting model 'CustList'
        db.delete_table(u'survey_custlist')

        # Deleting model 'CustListItem'
        db.delete_table(u'survey_custlistitem')

        # Removing M2M table for field defineInfo_set on 'CustListItem'
        db.delete_table(db.shorten_name(u'survey_custlistitem_defineInfo_set'))

        # Deleting model 'DefineInfo'
        db.delete_table(u'survey_defineinfo')


    models = {
        u'account.user': {
            'Meta': {'ordering': "['name']", 'object_name': 'User'},
            'birthDate': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'createBy': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'userCreated'", 'null': 'True', 'to': u"orm['account.User']"}),
            'createTime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 5, 29, 0, 0)'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modifyBy': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'userModified'", 'null': 'True', 'to': u"orm['account.User']"}),
            'modifyTime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 5, 29, 0, 0)'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'survey.branch': {
            'Meta': {'object_name': 'Branch'},
            'createBy': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'branchCreated_set'", 'to': u"orm['account.User']"}),
            'createTime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 5, 29, 0, 0)'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modifyBy': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'branchModified_set'", 'to': u"orm['account.User']"}),
            'modifyTime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 5, 29, 0, 0)'}),
            'nextQuestion': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'fromBranch'", 'null': 'True', 'to': u"orm['survey.Question']"}),
            'ord': ('django.db.models.fields.IntegerField', [], {}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['survey.Question']"}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'survey.custlist': {
            'Meta': {'object_name': 'CustList'},
            'createBy': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'custListCreated_set'", 'to': u"orm['account.User']"}),
            'createTime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 5, 29, 0, 0)'}),
            'descrition': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modifyBy': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'custListModified_set'", 'to': u"orm['account.User']"}),
            'modifyTime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 5, 29, 0, 0)'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'survey.custlistitem': {
            'Meta': {'object_name': 'CustListItem'},
            'createBy': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'custListItemCreated_set'", 'to': u"orm['account.User']"}),
            'createTime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 5, 29, 0, 0)'}),
            'custList': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'custListItem_set'", 'to': u"orm['survey.CustList']"}),
            'defineInfo_set': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['survey.DefineInfo']", 'symmetrical': 'False'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modifyBy': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'custListItemModified_set'", 'to': u"orm['account.User']"}),
            'modifyTime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 5, 29, 0, 0)'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'survey.defineinfo': {
            'Meta': {'object_name': 'DefineInfo'},
            'createBy': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'defineInfoCreated_set'", 'to': u"orm['account.User']"}),
            'createTime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 5, 29, 0, 0)'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modifyBy': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'defineInfoModified_set'", 'to': u"orm['account.User']"}),
            'modifyTime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 5, 29, 0, 0)'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'ord': ('django.db.models.fields.IntegerField', [], {}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'survey.paper': {
            'Meta': {'ordering': "['title']", 'object_name': 'Paper'},
            'createBy': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'paperCreated_set'", 'to': u"orm['account.User']"}),
            'createTime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 5, 29, 0, 0)'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inOrder': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'lookBack': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'modifyBy': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'paperModified_set'", 'to': u"orm['account.User']"}),
            'modifyTime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 5, 29, 0, 0)'}),
            'questionNumStyle': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'style': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        u'survey.papercatalog': {
            'Meta': {'object_name': 'PaperCatalog'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'createBy': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'paperCatalogCreated_set'", 'to': u"orm['account.User']"}),
            'createTime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 5, 29, 0, 0)'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modifyBy': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'paperCatalogModified_set'", 'to': u"orm['account.User']"}),
            'modifyTime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 5, 29, 0, 0)'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'ord': ('django.db.models.fields.IntegerField', [], {}),
            'paper_set': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['survey.Paper']", 'through': u"orm['survey.PaperCatalogPaper']", 'symmetrical': 'False'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['survey.PaperCatalog']", 'null': 'True', 'blank': 'True'})
        },
        u'survey.papercatalogpaper': {
            'Meta': {'object_name': 'PaperCatalogPaper'},
            'createBy': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'paperCatalogPaperCreated_set'", 'to': u"orm['account.User']"}),
            'createTime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 5, 29, 0, 0)'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modifyBy': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'paperCatalogPaperModified_set'", 'to': u"orm['account.User']"}),
            'modifyTime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 5, 29, 0, 0)'}),
            'ord': ('django.db.models.fields.IntegerField', [], {}),
            'paper': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['survey.Paper']"}),
            'paperCatalog': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['survey.PaperCatalog']"})
        },
        u'survey.question': {
            'Meta': {'ordering': "['ord']", 'object_name': 'Question'},
            'branchNumStyle': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'confused': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'contentLengh': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'createBy': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'questionCreated_set'", 'to': u"orm['account.User']"}),
            'createTime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 5, 29, 0, 0)'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modifyBy': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'questionModified_set'", 'to': u"orm['account.User']"}),
            'modifyTime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 5, 29, 0, 0)'}),
            'nextQuestion': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['survey.Question']", 'null': 'True', 'blank': 'True'}),
            'ord': ('django.db.models.fields.IntegerField', [], {}),
            'paper': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['survey.Paper']", 'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'valueMax': ('django.db.models.fields.FloatField', [], {'default': '10', 'null': 'True', 'blank': 'True'}),
            'valueMin': ('django.db.models.fields.FloatField', [], {'default': '0', 'null': 'True', 'blank': 'True'})
        },
        u'survey.questioncatalog': {
            'Meta': {'object_name': 'QuestionCatalog'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'createBy': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'questionCatalogCreated_set'", 'to': u"orm['account.User']"}),
            'createTime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 5, 29, 0, 0)'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modifyBy': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'questionCatalogModified_set'", 'to': u"orm['account.User']"}),
            'modifyTime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 5, 29, 0, 0)'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'ord': ('django.db.models.fields.IntegerField', [], {}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['survey.QuestionCatalog']", 'null': 'True', 'blank': 'True'}),
            'question_set': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['survey.Question']", 'through': u"orm['survey.QuestionCatalogQuestion']", 'symmetrical': 'False'})
        },
        u'survey.questioncatalogquestion': {
            'Meta': {'object_name': 'QuestionCatalogQuestion'},
            'createBy': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'questionCatalogQuestionCreated_set'", 'to': u"orm['account.User']"}),
            'createTime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 5, 29, 0, 0)'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modifyBy': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'questionCatalogQuestionModified_set'", 'to': u"orm['account.User']"}),
            'modifyTime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 5, 29, 0, 0)'}),
            'ord': ('django.db.models.fields.IntegerField', [], {}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['survey.Question']"}),
            'questionCatalog': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['survey.QuestionCatalog']"})
        },
        u'survey.resource': {
            'Meta': {'object_name': 'Resource'},
            'createBy': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'resourceCreated_set'", 'to': u"orm['account.User']"}),
            'createTime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 5, 29, 0, 0)'}),
            'height': ('django.db.models.fields.FloatField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modifyBy': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'resourceModified_set'", 'to': u"orm['account.User']"}),
            'modifyTime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 5, 29, 0, 0)'}),
            'resourceType': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'resourceUrl': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'stem': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['survey.Stem']"}),
            'width': ('django.db.models.fields.FloatField', [], {})
        },
        u'survey.sample': {
            'Meta': {'object_name': 'Sample'},
            'createBy': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sampleCreated_set'", 'to': u"orm['account.User']"}),
            'createTime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 5, 29, 0, 0)'}),
            'finished': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ipAddress': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'isValid': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'macAddress': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'modifyBy': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sampleModified_set'", 'to': u"orm['account.User']"}),
            'modifyTime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 5, 29, 0, 0)'}),
            'paper': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['survey.Paper']"}),
            'targetCust': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['survey.TargetCust']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['account.User']", 'null': 'True', 'blank': 'True'})
        },
        u'survey.sampleitem': {
            'Meta': {'object_name': 'SampleItem'},
            'branch_set': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['survey.Branch']", 'symmetrical': 'False'}),
            'content': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'createBy': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sampleItemCreated_set'", 'to': u"orm['account.User']"}),
            'createTime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 5, 29, 0, 0)'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modifyBy': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sampleItemModified_set'", 'to': u"orm['account.User']"}),
            'modifyTime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 5, 29, 0, 0)'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['survey.Question']"}),
            'sample': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['survey.Sample']"}),
            'score': ('django.db.models.fields.FloatField', [], {'default': '0'})
        },
        u'survey.stem': {
            'Meta': {'object_name': 'Stem'},
            'createBy': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'stemCreated_set'", 'to': u"orm['account.User']"}),
            'createTime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 5, 29, 0, 0)'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modifyBy': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'stemModified_set'", 'to': u"orm['account.User']"}),
            'modifyTime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 5, 29, 0, 0)'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['survey.Question']"}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '300'})
        },
        u'survey.survey': {
            'Meta': {'object_name': 'Survey'},
            'bonus': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'createBy': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'surveyCreated_set'", 'to': u"orm['account.User']"}),
            'createTime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 5, 29, 0, 0)'}),
            'endTime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 5, 29, 0, 0)'}),
            'fee': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'hardCost': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ipLimit': ('django.db.models.fields.IntegerField', [], {'default': '5'}),
            'macLimit': ('django.db.models.fields.IntegerField', [], {'default': '5'}),
            'modifyBy': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'surveyModified_set'", 'to': u"orm['account.User']"}),
            'modifyTime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 5, 29, 0, 0)'}),
            'paper': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['survey.Paper']"}),
            'passwd': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'publishTime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 5, 29, 0, 0)'}),
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
            'createTime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 5, 29, 0, 0)'}),
            'defineInfo_set': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['survey.DefineInfo']", 'symmetrical': 'False'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modifyBy': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'targetCustModified_set'", 'to': u"orm['account.User']"}),
            'modifyTime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 5, 29, 0, 0)'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'survey': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'targetCust_set'", 'to': u"orm['survey.Survey']"}),
            'token': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['survey']