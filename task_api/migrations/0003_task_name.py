# Generated by Django 4.0.6 on 2022-08-27 00:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task_api', '0002_remove_task_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='name',
            field=models.CharField(default='Task', max_length=100),
            preserve_default=False,
        ),
    ]
