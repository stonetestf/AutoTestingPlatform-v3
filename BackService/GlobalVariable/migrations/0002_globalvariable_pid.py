# Generated by Django 2.2.24 on 2021-12-08 12:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ProjectManagement', '0009_delete_history'),
        ('GlobalVariable', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='globalvariable',
            name='pid',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='ProjectManagement.ProManagement'),
            preserve_default=False,
        ),
    ]