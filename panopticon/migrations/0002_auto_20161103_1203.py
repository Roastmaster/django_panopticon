# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-03 16:03
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('panopticon', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='crewlead',
            name='employee',
        ),
        migrations.RemoveField(
            model_name='crewlead',
            name='sector',
        ),
        migrations.RemoveField(
            model_name='farmemployee',
            name='farm',
        ),
        migrations.RemoveField(
            model_name='farmemployee',
            name='user',
        ),
        migrations.RemoveField(
            model_name='farmowner',
            name='employee',
        ),
        migrations.RemoveField(
            model_name='farmowner',
            name='farm',
        ),
        migrations.RemoveField(
            model_name='incident',
            name='employees_involved',
        ),
        migrations.RemoveField(
            model_name='incident',
            name='farm',
        ),
        migrations.RemoveField(
            model_name='incident',
            name='reporter',
        ),
        migrations.RemoveField(
            model_name='incident',
            name='sector',
        ),
        migrations.RemoveField(
            model_name='sector',
            name='farm',
        ),
        migrations.RemoveField(
            model_name='squad',
            name='lead',
        ),
        migrations.DeleteModel(
            name='CrewLead',
        ),
        migrations.DeleteModel(
            name='Farm',
        ),
        migrations.DeleteModel(
            name='FarmEmployee',
        ),
        migrations.DeleteModel(
            name='FarmOwner',
        ),
        migrations.DeleteModel(
            name='Incident',
        ),
        migrations.DeleteModel(
            name='Sector',
        ),
        migrations.DeleteModel(
            name='Squad',
        ),
    ]
