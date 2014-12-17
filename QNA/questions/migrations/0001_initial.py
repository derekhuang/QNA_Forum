# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import questions.models.utils


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('author', models.CharField(max_length=50)),
                ('body', models.TextField()),
                ('published_time', models.DateTimeField()),
                ('view_amount', models.IntegerField(default=0)),
                ('like', models.IntegerField(default=0)),
                ('dislike', models.IntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('author', models.CharField(max_length=50)),
                ('body', models.TextField()),
                ('published_time', models.DateTimeField()),
                ('view_amount', models.IntegerField(default=0)),
                ('answer', models.ForeignKey(to='questions.Answer')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='KeyValue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key', models.CharField(unique=True, max_length=255)),
                ('value', questions.models.utils.PickledObjectField(null=True, editable=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('author', models.CharField(max_length=50)),
                ('body', models.TextField()),
                ('published_time', models.DateTimeField()),
                ('view_amount', models.IntegerField(default=0)),
                ('stock_id', models.CharField(max_length=10)),
                ('title', models.CharField(max_length=100)),
                ('catetory', models.IntegerField()),
                ('sub_tag', models.IntegerField(blank=True)),
                ('like', models.IntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('description', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='question',
            name='tag',
            field=models.ForeignKey(to='questions.Tag'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(to='questions.Question'),
            preserve_default=True,
        ),
    ]
