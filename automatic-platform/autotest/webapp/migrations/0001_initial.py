# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Action',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('desc', models.CharField(max_length=1000)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Ap',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=200)),
                ('create_date', models.DateTimeField(auto_now=True)),
                ('edit_date', models.CharField(max_length=200)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ap_detail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=500)),
                ('case_type', models.CharField(max_length=200)),
                ('create_date', models.DateTimeField(auto_now=True)),
                ('edit_date', models.CharField(max_length=200)),
                ('ap', models.ForeignKey(to='webapp.Ap')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='api_business',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('create_date', models.DateTimeField(auto_now=True)),
                ('edit_date', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='api_detail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('create_date', models.DateTimeField(auto_now=True)),
                ('api', models.ForeignKey(to='webapp.api_business')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Business',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=200)),
                ('date', models.DateTimeField(auto_now=True)),
                ('category', models.CharField(max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Business_stp',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('case_id', models.CharField(max_length=200)),
                ('date', models.DateTimeField(auto_now=True)),
                ('case_nature', models.CharField(max_length=200)),
                ('business', models.ForeignKey(to='webapp.Business')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Case',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=200)),
                ('browser', models.CharField(max_length=500)),
                ('date', models.DateTimeField(auto_now=True)),
                ('case_nature', models.CharField(max_length=500)),
                ('category', models.CharField(max_length=200)),
                ('status', models.CharField(max_length=200)),
                ('features', models.CharField(max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='case_process',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('desc', models.CharField(max_length=500)),
                ('action', models.CharField(max_length=200)),
                ('value', models.CharField(max_length=200)),
                ('ele_id', models.CharField(max_length=20)),
                ('ele_name', models.CharField(max_length=200)),
                ('case', models.ForeignKey(to='webapp.Case')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Caseaction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('actor', models.CharField(max_length=300)),
                ('ac_type', models.CharField(max_length=300)),
                ('ac_date', models.DateTimeField(auto_now=True)),
                ('action', models.CharField(max_length=300)),
                ('edit_field', models.CharField(max_length=300)),
                ('old_field_value', models.CharField(max_length=300)),
                ('new_field_value', models.CharField(max_length=300)),
                ('debug_result', models.CharField(max_length=300)),
                ('case', models.ForeignKey(to='webapp.Case')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Diff',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('objId', models.CharField(max_length=20)),
                ('field_name', models.CharField(max_length=200)),
                ('diffType', models.CharField(max_length=20)),
                ('value', models.CharField(max_length=200)),
                ('ex', models.CharField(max_length=2000)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='element',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('fun', models.CharField(max_length=200)),
                ('values', models.CharField(max_length=500)),
                ('desc', models.CharField(max_length=500)),
                ('page_url', models.CharField(max_length=500)),
                ('creator', models.CharField(max_length=300)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Elementaction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('actor', models.CharField(max_length=300)),
                ('actiondate', models.DateTimeField(auto_now=True)),
                ('action', models.CharField(max_length=300)),
                ('edit_field', models.CharField(max_length=500)),
                ('old_field_value', models.CharField(max_length=500)),
                ('new_field_value', models.CharField(max_length=500)),
                ('element', models.ForeignKey(to='webapp.element')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Execution_detail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('case_nature', models.CharField(max_length=500)),
                ('category', models.CharField(max_length=100)),
                ('date', models.DateTimeField(auto_now=True)),
                ('case_id', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Historyaction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('actor', models.CharField(max_length=300)),
                ('ac_type', models.CharField(max_length=300)),
                ('ac_date', models.DateTimeField(auto_now=True)),
                ('action', models.CharField(max_length=300)),
                ('edit_field', models.CharField(max_length=300)),
                ('old_field_value', models.CharField(max_length=300)),
                ('new_field_value', models.CharField(max_length=300)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='InCaseDetail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('objId', models.CharField(max_length=20)),
                ('value', models.CharField(max_length=1000)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='InCaseList',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tempId', models.CharField(max_length=10)),
                ('caseName', models.CharField(unique=True, max_length=200)),
                ('creator', models.CharField(max_length=300)),
                ('createDate', models.DateTimeField(auto_now_add=True)),
                ('modifyDate', models.CharField(max_length=100)),
                ('status', models.CharField(max_length=100)),
                ('nature', models.CharField(max_length=300)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Method',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=200)),
                ('create_time', models.DateTimeField(auto_now=True)),
                ('pro_user', models.CharField(max_length=200)),
                ('pro_status', models.CharField(max_length=200)),
                ('url', models.CharField(max_length=500)),
                ('test_type', models.CharField(default=b'Web\xe6\xb5\x8b\xe8\xaf\x95', max_length=20)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProSetting',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('envName', models.CharField(max_length=200)),
                ('address', models.CharField(max_length=200)),
                ('port', models.CharField(max_length=20)),
                ('connectType', models.CharField(max_length=40)),
                ('connectData', models.CharField(max_length=40)),
                ('userName', models.CharField(max_length=30)),
                ('passWord', models.CharField(max_length=30)),
                ('interfaceType', models.CharField(max_length=20)),
                ('is_used', models.CharField(default=False, max_length=10)),
                ('proName', models.ForeignKey(to='webapp.Project')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProTemp',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tempName', models.CharField(unique=True, max_length=200)),
                ('createTime', models.DateTimeField(auto_now=True)),
                ('last_time', models.CharField(max_length=100)),
                ('createUser', models.CharField(max_length=40)),
                ('template_type', models.CharField(max_length=100)),
                ('proName', models.ForeignKey(to='webapp.Project')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TempDetail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('objName', models.CharField(max_length=120)),
                ('part', models.CharField(max_length=40)),
                ('list', models.CharField(max_length=40)),
                ('key', models.CharField(max_length=40)),
                ('key2', models.CharField(max_length=40)),
                ('type', models.CharField(max_length=40)),
                ('temp', models.ForeignKey(to='webapp.ProTemp')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Test_execution',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=200, error_messages={b'msg': b'\xe9\x87\x8d\xe5\xa4\x8d'})),
                ('date', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Test_report',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('Execution_id', models.CharField(max_length=20)),
                ('date', models.CharField(max_length=200)),
                ('path', models.CharField(max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='incaselist',
            name='project',
            field=models.ForeignKey(to='webapp.Project'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='incasedetail',
            name='case',
            field=models.ForeignKey(to='webapp.InCaseList'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='historyaction',
            name='Project',
            field=models.ForeignKey(to='webapp.Project'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='execution_detail',
            name='perform',
            field=models.ForeignKey(to='webapp.Test_execution'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='element',
            name='project',
            field=models.ForeignKey(to='webapp.Project', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='diff',
            name='case',
            field=models.ForeignKey(to='webapp.InCaseList'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='case',
            name='project',
            field=models.ForeignKey(to='webapp.Project'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='business',
            name='Project',
            field=models.ForeignKey(to='webapp.Project'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='api_detail',
            name='case',
            field=models.ForeignKey(to='webapp.InCaseList', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='api_business',
            name='pro',
            field=models.ForeignKey(to='webapp.Project'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='api_business',
            unique_together=set([('name',)]),
        ),
        migrations.AddField(
            model_name='ap_detail',
            name='api',
            field=models.ForeignKey(to='webapp.api_business', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ap_detail',
            name='case',
            field=models.ForeignKey(to='webapp.InCaseList', null=True),
            preserve_default=True,
        ),
    ]
