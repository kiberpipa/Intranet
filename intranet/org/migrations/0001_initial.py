# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Tag'
        db.create_table('org_tag', (
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200, primary_key='True')),
            ('total_ref', self.gf('django.db.models.fields.IntegerField')(default=0, blank=True)),
            ('font_size', self.gf('django.db.models.fields.IntegerField')(default=0, blank=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['org.Tag'], null=True, blank=True)),
        ))
        db.send_create_signal('org', ['Tag'])

        # Adding model 'ProjectAudit'
        db.create_table('org_project_audit', (
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('responsible', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
            ('note', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True, blank=True)),
            ('salary_rate', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('verbose_name', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['org.Project'], null=True, blank=True)),
            ('salary_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mercenaries.SalaryType'], null=True, blank=True)),
            ('cost_center', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mercenaries.CostCenter'], null=True, blank=True)),
            ('pub_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('chg_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('email_members', self.gf('django.db.models.fields.NullBooleanField')(default=True, null=True, blank=True)),
            ('_audit_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('_audit_timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('_audit_change_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('id', self.gf('django.db.models.fields.IntegerField')(db_index=True)),
        ))
        db.send_create_signal('org', ['ProjectAudit'])

        # Adding model 'Project'
        db.create_table('org_project', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('responsible', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
            ('note', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True, blank=True)),
            ('salary_rate', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('verbose_name', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['org.Project'], null=True, blank=True)),
            ('salary_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mercenaries.SalaryType'], null=True, blank=True)),
            ('cost_center', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mercenaries.CostCenter'], null=True, blank=True)),
            ('pub_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('chg_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('email_members', self.gf('django.db.models.fields.NullBooleanField')(default=True, null=True, blank=True)),
        ))
        db.send_create_signal('org', ['Project'])

        # Adding model 'Category'
        db.create_table('org_category', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('note', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('pub_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('chg_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('org', ['Category'])

        # Adding model 'Place'
        db.create_table('org_place', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('note', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('org', ['Place'])

        # Adding model 'EmailBlacklist'
        db.create_table('org_emailblacklist', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('blacklisted', self.gf('django.db.models.fields.EmailField')(unique=True, max_length=75, db_index=True)),
        ))
        db.send_create_signal('org', ['EmailBlacklist'])

        # Adding model 'Email'
        db.create_table('org_email', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
        ))
        db.send_create_signal('org', ['Email'])

        # Adding model 'Phone'
        db.create_table('org_phone', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('org', ['Phone'])

        # Adding model 'Organization'
        db.create_table('org_organization', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('organization', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('org', ['Organization'])

        # Adding model 'Role'
        db.create_table('org_role', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('role', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('org', ['Role'])

        # Adding model 'IntranetImage'
        db.create_table('org_intranetimage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('md5', self.gf('django.db.models.fields.CharField')(db_index=True, unique=True, max_length=32, blank=True)),
        ))
        db.send_create_signal('org', ['IntranetImage'])

        # Adding model 'Event'
        db.create_table('org_event', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('responsible', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('slug', self.gf('django.db.models.fields.SlugField')(db_index=True, max_length=150, null=True, blank=True)),
            ('start_date', self.gf('django.db.models.fields.DateTimeField')(db_index=True)),
            ('end_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('length', self.gf('django.db.models.fields.TimeField')()),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['org.Project'])),
            ('require_technician', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('require_video', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('visitors', self.gf('django.db.models.fields.IntegerField')(default=0, null=True, blank=True)),
            ('public', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('language', self.gf('django.db.models.fields.CharField')(default='sl', max_length=2, null=True, blank=True)),
            ('sequence', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('slides', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
            ('announce', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('short_announce', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('note', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('pub_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('chg_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('place', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['org.Place'])),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['org.Category'])),
            ('event_image', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['org.IntranetImage'], null=True, blank=True)),
        ))
        db.send_create_signal('org', ['Event'])

        # Adding M2M table for field technician on 'Event'
        db.create_table('org_event_technician', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('event', models.ForeignKey(orm['org.event'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique('org_event_technician', ['event_id', 'user_id'])

        # Adding M2M table for field tags on 'Event'
        db.create_table('org_event_tags', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('event', models.ForeignKey(orm['org.event'], null=False)),
            ('tag', models.ForeignKey(orm['org.tag'], null=False))
        ))
        db.create_unique('org_event_tags', ['event_id', 'tag_id'])

        # Adding M2M table for field emails on 'Event'
        db.create_table('org_event_emails', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('event', models.ForeignKey(orm['org.event'], null=False)),
            ('email', models.ForeignKey(orm['org.email'], null=False))
        ))
        db.create_unique('org_event_emails', ['event_id', 'email_id'])

        # Adding model 'TipSodelovanja'
        db.create_table('org_tipsodelovanja', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=40)),
        ))
        db.send_create_signal('org', ['TipSodelovanja'])

        # Adding model 'Person'
        db.create_table('org_person', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('note', self.gf('django.db.models.fields.CharField')(max_length=230, null=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal('org', ['Person'])

        # Adding M2M table for field email on 'Person'
        db.create_table('org_person_email', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('person', models.ForeignKey(orm['org.person'], null=False)),
            ('email', models.ForeignKey(orm['org.email'], null=False))
        ))
        db.create_unique('org_person_email', ['person_id', 'email_id'])

        # Adding M2M table for field phone on 'Person'
        db.create_table('org_person_phone', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('person', models.ForeignKey(orm['org.person'], null=False)),
            ('phone', models.ForeignKey(orm['org.phone'], null=False))
        ))
        db.create_unique('org_person_phone', ['person_id', 'phone_id'])

        # Adding M2M table for field organization on 'Person'
        db.create_table('org_person_organization', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('person', models.ForeignKey(orm['org.person'], null=False)),
            ('organization', models.ForeignKey(orm['org.organization'], null=False))
        ))
        db.create_unique('org_person_organization', ['person_id', 'organization_id'])

        # Adding M2M table for field role on 'Person'
        db.create_table('org_person_role', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('person', models.ForeignKey(orm['org.person'], null=False)),
            ('role', models.ForeignKey(orm['org.role'], null=False))
        ))
        db.create_unique('org_person_role', ['person_id', 'role_id'])

        # Adding model 'Sodelovanje'
        db.create_table('org_sodelovanje', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['org.Event'], null=True, blank=True)),
            ('tip', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['org.TipSodelovanja'], null=True, blank=True)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['org.Person'])),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['org.Project'], null=True, blank=True)),
            ('note', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('org', ['Sodelovanje'])

        # Adding model 'Task'
        db.create_table('org_task', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('responsible', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
            ('note', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('pub_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('chg_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('org', ['Task'])

        # Adding model 'Diary'
        db.create_table('org_diary', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(related_name='diary_author', to=orm['auth.User'])),
            ('task', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['org.Project'])),
            ('date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.date(2010, 11, 8), db_index=True)),
            ('length', self.gf('django.db.models.fields.TimeField')(default=datetime.time(4, 0))),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['org.Event'], null=True, blank=True)),
            ('log_formal', self.gf('django.db.models.fields.TextField')()),
            ('log_informal', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('pub_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('chg_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('org', ['Diary'])

        # Adding M2M table for field tags on 'Diary'
        db.create_table('org_diary_tags', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('diary', models.ForeignKey(orm['org.diary'], null=False)),
            ('tag', models.ForeignKey(orm['org.tag'], null=False))
        ))
        db.create_unique('org_diary_tags', ['diary_id', 'tag_id'])

        # Adding model 'StickyNote'
        db.create_table('org_stickynote', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(related_name='message_author', to=orm['auth.User'])),
            ('post_date', self.gf('django.db.models.fields.DateField')(default=datetime.date(2010, 11, 8))),
            ('due_date', self.gf('django.db.models.fields.DateField')(default=datetime.date(2010, 11, 13))),
            ('note', self.gf('django.db.models.fields.TextField')()),
            ('pub_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('chg_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('org', ['StickyNote'])

        # Adding M2M table for field tags on 'StickyNote'
        db.create_table('org_stickynote_tags', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('stickynote', models.ForeignKey(orm['org.stickynote'], null=False)),
            ('tag', models.ForeignKey(orm['org.tag'], null=False))
        ))
        db.create_unique('org_stickynote_tags', ['stickynote_id', 'tag_id'])

        # Adding model 'Lend'
        db.create_table('org_lend', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('what', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('to_who', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('from_who', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('from_date', self.gf('django.db.models.fields.DateField')(default=datetime.date(2010, 11, 8))),
            ('due_date', self.gf('django.db.models.fields.DateField')(default=datetime.date(2010, 11, 9))),
            ('contact_info', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('why', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('returned', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('note', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('pub_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('chg_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('org', ['Lend'])

        # Adding model 'KbCategory'
        db.create_table('org_kbcategory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=75, db_index=True)),
            ('pub_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('chg_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('org', ['KbCategory'])

        # Adding model 'KB'
        db.create_table('org_kb', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=75, db_index=True)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['org.KbCategory'])),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('editor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('pub_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('chg_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('org', ['KB'])

        # Adding M2M table for field project on 'KB'
        db.create_table('org_kb_project', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('kb', models.ForeignKey(orm['org.kb'], null=False)),
            ('project', models.ForeignKey(orm['org.project'], null=False))
        ))
        db.create_unique('org_kb_project', ['kb_id', 'project_id'])

        # Adding M2M table for field task on 'KB'
        db.create_table('org_kb_task', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('kb', models.ForeignKey(orm['org.kb'], null=False)),
            ('task', models.ForeignKey(orm['org.task'], null=False))
        ))
        db.create_unique('org_kb_task', ['kb_id', 'task_id'])

        # Adding model 'Shopping'
        db.create_table('org_shopping', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(related_name='shopping_author', to=orm['auth.User'])),
            ('explanation', self.gf('django.db.models.fields.TextField')()),
            ('cost', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=10, decimal_places=2, blank=True)),
            ('bought', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('responsible', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='shopping_responsible', null=True, to=orm['auth.User'])),
            ('pub_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('chg_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('org', ['Shopping'])

        # Adding M2M table for field supporters on 'Shopping'
        db.create_table('org_shopping_supporters', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('shopping', models.ForeignKey(orm['org.shopping'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique('org_shopping_supporters', ['shopping_id', 'user_id'])

        # Adding M2M table for field project on 'Shopping'
        db.create_table('org_shopping_project', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('shopping', models.ForeignKey(orm['org.shopping'], null=False)),
            ('project', models.ForeignKey(orm['org.project'], null=False))
        ))
        db.create_unique('org_shopping_project', ['shopping_id', 'project_id'])

        # Adding M2M table for field tags on 'Shopping'
        db.create_table('org_shopping_tags', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('shopping', models.ForeignKey(orm['org.shopping'], null=False)),
            ('tag', models.ForeignKey(orm['org.tag'], null=False))
        ))
        db.create_unique('org_shopping_tags', ['shopping_id', 'tag_id'])

        # Adding model 'Scratchpad'
        db.create_table('org_scratchpad', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('pub_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('chg_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('org', ['Scratchpad'])


    def backwards(self, orm):
        
        # Deleting model 'Tag'
        db.delete_table('org_tag')

        # Deleting model 'ProjectAudit'
        db.delete_table('org_project_audit')

        # Deleting model 'Project'
        db.delete_table('org_project')

        # Deleting model 'Category'
        db.delete_table('org_category')

        # Deleting model 'Place'
        db.delete_table('org_place')

        # Deleting model 'EmailBlacklist'
        db.delete_table('org_emailblacklist')

        # Deleting model 'Email'
        db.delete_table('org_email')

        # Deleting model 'Phone'
        db.delete_table('org_phone')

        # Deleting model 'Organization'
        db.delete_table('org_organization')

        # Deleting model 'Role'
        db.delete_table('org_role')

        # Deleting model 'IntranetImage'
        db.delete_table('org_intranetimage')

        # Deleting model 'Event'
        db.delete_table('org_event')

        # Removing M2M table for field technician on 'Event'
        db.delete_table('org_event_technician')

        # Removing M2M table for field tags on 'Event'
        db.delete_table('org_event_tags')

        # Removing M2M table for field emails on 'Event'
        db.delete_table('org_event_emails')

        # Deleting model 'TipSodelovanja'
        db.delete_table('org_tipsodelovanja')

        # Deleting model 'Person'
        db.delete_table('org_person')

        # Removing M2M table for field email on 'Person'
        db.delete_table('org_person_email')

        # Removing M2M table for field phone on 'Person'
        db.delete_table('org_person_phone')

        # Removing M2M table for field organization on 'Person'
        db.delete_table('org_person_organization')

        # Removing M2M table for field role on 'Person'
        db.delete_table('org_person_role')

        # Deleting model 'Sodelovanje'
        db.delete_table('org_sodelovanje')

        # Deleting model 'Task'
        db.delete_table('org_task')

        # Deleting model 'Diary'
        db.delete_table('org_diary')

        # Removing M2M table for field tags on 'Diary'
        db.delete_table('org_diary_tags')

        # Deleting model 'StickyNote'
        db.delete_table('org_stickynote')

        # Removing M2M table for field tags on 'StickyNote'
        db.delete_table('org_stickynote_tags')

        # Deleting model 'Lend'
        db.delete_table('org_lend')

        # Deleting model 'KbCategory'
        db.delete_table('org_kbcategory')

        # Deleting model 'KB'
        db.delete_table('org_kb')

        # Removing M2M table for field project on 'KB'
        db.delete_table('org_kb_project')

        # Removing M2M table for field task on 'KB'
        db.delete_table('org_kb_task')

        # Deleting model 'Shopping'
        db.delete_table('org_shopping')

        # Removing M2M table for field supporters on 'Shopping'
        db.delete_table('org_shopping_supporters')

        # Removing M2M table for field project on 'Shopping'
        db.delete_table('org_shopping_project')

        # Removing M2M table for field tags on 'Shopping'
        db.delete_table('org_shopping_tags')

        # Deleting model 'Scratchpad'
        db.delete_table('org_scratchpad')


    models = {
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
        },
        'mercenaries.costcenter': {
            'Meta': {'object_name': 'CostCenter'},
            'code': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'wage_per_hour': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'})
        },
        'mercenaries.salarytype': {
            'Meta': {'object_name': 'SalaryType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'org.category': {
            'Meta': {'object_name': 'Category'},
            'chg_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'note': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        'org.diary': {
            'Meta': {'object_name': 'Diary'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'diary_author'", 'to': "orm['auth.User']"}),
            'chg_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.date(2010, 11, 8)', 'db_index': 'True'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['org.Event']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'length': ('django.db.models.fields.TimeField', [], {'default': 'datetime.time(4, 0)'}),
            'log_formal': ('django.db.models.fields.TextField', [], {}),
            'log_informal': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['org.Tag']", 'null': 'True', 'blank': 'True'}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['org.Project']"})
        },
        'org.email': {
            'Meta': {'object_name': 'Email'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'org.emailblacklist': {
            'Meta': {'object_name': 'EmailBlacklist'},
            'blacklisted': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'org.event': {
            'Meta': {'ordering': "('title',)", 'object_name': 'Event'},
            'announce': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['org.Category']"}),
            'chg_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'emails': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['org.Email']", 'null': 'True', 'blank': 'True'}),
            'end_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'event_image': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['org.IntranetImage']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'default': "'sl'", 'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'length': ('django.db.models.fields.TimeField', [], {}),
            'note': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'place': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['org.Place']"}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['org.Project']"}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'require_technician': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'require_video': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'responsible': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'sequence': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'short_announce': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'slides': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'db_index': 'True', 'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['org.Tag']", 'null': 'True', 'blank': 'True'}),
            'technician': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'event_technican'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['auth.User']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'visitors': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'})
        },
        'org.intranetimage': {
            'Meta': {'ordering': "('-image',)", 'object_name': 'IntranetImage'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'md5': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'unique': 'True', 'max_length': '32', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'org.kb': {
            'Meta': {'object_name': 'KB'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['org.KbCategory']"}),
            'chg_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'editor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['org.Project']", 'null': 'True', 'blank': 'True'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '75', 'db_index': 'True'}),
            'task': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['org.Task']", 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '150'})
        },
        'org.kbcategory': {
            'Meta': {'object_name': 'KbCategory'},
            'chg_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '75', 'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '150'})
        },
        'org.lend': {
            'Meta': {'object_name': 'Lend'},
            'chg_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'contact_info': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'due_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.date(2010, 11, 9)'}),
            'from_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.date(2010, 11, 8)'}),
            'from_who': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'note': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'returned': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'to_who': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'what': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'why': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'org.organization': {
            'Meta': {'object_name': 'Organization'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'organization': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'org.person': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Person'},
            'email': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['org.Email']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'note': ('django.db.models.fields.CharField', [], {'max_length': '230', 'null': 'True', 'blank': 'True'}),
            'organization': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['org.Organization']", 'null': 'True', 'blank': 'True'}),
            'phone': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['org.Phone']", 'null': 'True', 'blank': 'True'}),
            'role': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['org.Role']", 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'org.phone': {
            'Meta': {'object_name': 'Phone'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'org.place': {
            'Meta': {'object_name': 'Place'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'note': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        'org.project': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Project'},
            'chg_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'cost_center': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mercenaries.CostCenter']", 'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'email_members': ('django.db.models.fields.NullBooleanField', [], {'default': 'True', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'note': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['org.Project']", 'null': 'True', 'blank': 'True'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'responsible': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'salary_rate': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'salary_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mercenaries.SalaryType']", 'null': 'True', 'blank': 'True'}),
            'verbose_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'org.projectaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'ProjectAudit', 'db_table': "'org_project_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'chg_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'cost_center': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mercenaries.CostCenter']", 'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'email_members': ('django.db.models.fields.NullBooleanField', [], {'default': 'True', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'note': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['org.Project']", 'null': 'True', 'blank': 'True'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'responsible': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'salary_rate': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'salary_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mercenaries.SalaryType']", 'null': 'True', 'blank': 'True'}),
            'verbose_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'org.role': {
            'Meta': {'object_name': 'Role'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'role': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'org.scratchpad': {
            'Meta': {'object_name': 'Scratchpad'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'chg_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        'org.shopping': {
            'Meta': {'object_name': 'Shopping'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'shopping_author'", 'to': "orm['auth.User']"}),
            'bought': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'chg_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'cost': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            'explanation': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'project': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['org.Project']", 'null': 'True', 'blank': 'True'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'responsible': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'shopping_responsible'", 'null': 'True', 'to': "orm['auth.User']"}),
            'supporters': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'shopping_supporters'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['auth.User']"}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['org.Tag']", 'null': 'True', 'blank': 'True'})
        },
        'org.sodelovanje': {
            'Meta': {'ordering': "('-event__start_date',)", 'object_name': 'Sodelovanje'},
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['org.Event']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'note': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['org.Person']"}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['org.Project']", 'null': 'True', 'blank': 'True'}),
            'tip': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['org.TipSodelovanja']", 'null': 'True', 'blank': 'True'})
        },
        'org.stickynote': {
            'Meta': {'object_name': 'StickyNote'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'message_author'", 'to': "orm['auth.User']"}),
            'chg_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'due_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.date(2010, 11, 13)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'note': ('django.db.models.fields.TextField', [], {}),
            'post_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.date(2010, 11, 8)'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['org.Tag']", 'null': 'True', 'blank': 'True'})
        },
        'org.tag': {
            'Meta': {'object_name': 'Tag'},
            'font_size': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'primary_key': "'True'"}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['org.Tag']", 'null': 'True', 'blank': 'True'}),
            'total_ref': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'})
        },
        'org.task': {
            'Meta': {'object_name': 'Task'},
            'chg_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'note': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'responsible': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'org.tipsodelovanja': {
            'Meta': {'object_name': 'TipSodelovanja'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40'})
        }
    }

    complete_apps = ['org']
