# Generated by Django 2.2.24 on 2022-01-07 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Api_TestReport', '0013_auto_20211228_1510'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='apiqueue',
            name='fun',
        ),
        migrations.RemoveField(
            model_name='apiqueue',
            name='page',
        ),
        migrations.AddField(
            model_name='apiqueue',
            name='fun_id',
            field=models.IntegerField(null=True, verbose_name='所属功能'),
        ),
        migrations.AddField(
            model_name='apiqueue',
            name='page_id',
            field=models.IntegerField(null=True, verbose_name='所属页面'),
        ),
    ]
