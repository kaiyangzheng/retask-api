from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models 

# Create your models here.
class CustomUser(AbstractUser):
    task_type_preferences = models.JSONField(default=list)
    friends = models.ManyToManyField('self', blank=True)
    
    def __str__(self):
        return self.username
    