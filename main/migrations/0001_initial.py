# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-22 19:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contribution',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contribution_text', models.TextField()),
                ('submitted_at', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Story',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
            ],
        ),
        migrations.AddField(
            model_name='contribution',
            name='story',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Story'),
        ),
    ]
