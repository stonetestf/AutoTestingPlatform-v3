# Generated by Django 2.2.24 on 2022-01-07 15:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Api_TimingTask', '0013_auto_20220107_1534'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='apitimingtask',
            name='historyCode',
        ),
    ]
