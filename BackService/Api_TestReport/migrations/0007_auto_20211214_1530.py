# Generated by Django 2.2.24 on 2021-12-14 15:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Api_TestReport', '0006_apiqueue'),
    ]

    operations = [
        migrations.RenameField(
            model_name='apiqueue',
            old_name='report',
            new_name='testReport',
        ),
    ]