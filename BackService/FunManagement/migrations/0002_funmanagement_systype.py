# Generated by Django 2.2.24 on 2021-12-01 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FunManagement', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='funmanagement',
            name='sysType',
            field=models.CharField(default=1, max_length=10, verbose_name='所属系统'),
            preserve_default=False,
        ),
    ]
