# Generated by Django 3.0.9 on 2022-06-24 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0006_auto_20220624_1559'),
    ]

    operations = [
        migrations.AddField(
            model_name='userregistrationmodel',
            name='angelemail',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
