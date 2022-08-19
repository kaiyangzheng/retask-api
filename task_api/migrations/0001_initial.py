# Generated by Django 4.0.6 on 2022-07-30 12:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ReviewSession',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('quality', models.IntegerField(default=0)),
                ('ease_factor', models.FloatField(default=2.5)),
                ('time_started', models.DateTimeField(auto_now_add=True)),
                ('time_finished', models.DateTimeField(blank=True, null=True)),
                ('time_elapsed', models.IntegerField(default=0)),
                ('completed', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('quality', models.IntegerField(default=0)),
                ('repetitions', models.IntegerField(default=0)),
                ('ease_factor', models.FloatField(default=2.5)),
                ('prev_review_date', models.DateTimeField(blank=True, null=True)),
                ('next_review_date', models.DateTimeField(blank=True, null=True)),
                ('interval', models.IntegerField(default=0)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('review_sessions', models.ManyToManyField(blank=True, related_name='tasks', to='task_api.reviewsession')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='reviewsession',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='task_api.task'),
        ),
        migrations.AddField(
            model_name='reviewsession',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Goal',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('average_quality', models.FloatField(default=4)),
                ('average_time_spent', models.FloatField(default=600)),
                ('average_repetitions', models.IntegerField(default=3)),
                ('total_added', models.IntegerField(default=5)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('deadline', models.DateTimeField(blank=True, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
