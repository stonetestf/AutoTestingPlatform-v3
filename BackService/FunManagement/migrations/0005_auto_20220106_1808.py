# Generated by Django 2.2.24 on 2022-01-06 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FunManagement', '0004_funhistory_fun'),
    ]

    operations = [
        migrations.AlterField(
            model_name='funmanagement',
            name='remarks',
            field=models.TextField(null=True, verbose_name='备注信息'),
        ),
    ]
