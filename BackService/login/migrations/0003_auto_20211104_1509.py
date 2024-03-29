# Generated by Django 3.2.9 on 2021-11-04 07:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0002_errormsg'),
    ]

    operations = [
        migrations.AlterField(
            model_name='errormsg',
            name='sys',
            field=models.CharField(max_length=10, verbose_name='测试类型(Login/Int/Fun/Per)'),
        ),
        migrations.AlterField(
            model_name='usertable',
            name='nickName',
            field=models.CharField(default=1, max_length=200),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='usertable',
            name='userName',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
    ]
