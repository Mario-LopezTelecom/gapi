# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-09 15:01
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import oauth2client.contrib.django_orm


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CredentialsModel',
            fields=[
                ('id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('credential', oauth2client.contrib.django_orm.CredentialsField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='FlowModel',
            fields=[
                ('id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('flow', oauth2client.contrib.django_orm.FlowField(null=True)),
            ],
        ),
    ]
