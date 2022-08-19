from django.contrib import admin
from .models import Task, ReviewSession, Goal

# Register your models here.
admin.site.register(Task)
admin.site.register(ReviewSession)
admin.site.register(Goal)