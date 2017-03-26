# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('question_name', models.CharField(max_length=100)),
                ('question_text', models.CharField(max_length=3000)),
            ],
        ),
        migrations.CreateModel(
            name='QuestionData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('score', models.IntegerField(default=0)),
                ('timereq', models.IntegerField(default=0)),
                ('question', models.ForeignKey(to='ncc.Question')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name1', models.CharField(max_length=30)),
                ('name2', models.CharField(max_length=30, blank=True)),
                ('score', models.IntegerField(default=0)),
                ('subid', models.IntegerField(default=0)),
                ('start', models.DateTimeField(default=django.utils.timezone.now)),
                ('totaltime', models.IntegerField(default=0)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
