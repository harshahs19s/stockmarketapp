# Generated by Django 3.0.9 on 2022-06-24 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0005_userregistrationmodel_angelonestatus'),
    ]

    operations = [
        migrations.AddField(
            model_name='userregistrationmodel',
            name='angelmobile',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='userregistrationmodel',
            name='angelname',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='userregistrationmodel',
            name='client_code',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='userregistrationmodel',
            name='token',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
