from django.db import models
from authentication.models import CustomUser 
# Create your models here.
class Task(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True, default='')
    quality = models.IntegerField(default=0)
    repetitions = models.IntegerField(default=0)
    ease_factor = models.FloatField(default=2.5)
    prev_review_date = models.DateTimeField(null=True, blank=True)
    next_review_date = models.DateTimeField(null=True, blank=True)
    interval = models.IntegerField(default=0)
    favorite = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True)
    review_sessions = models.ManyToManyField('ReviewSession', blank=True, related_name='tasks')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)

    def update(self, quality, repetitions, ease_factor, interval, next_review_date, prev_review_date, review_session):
        self.quality = quality
        self.repetitions = repetitions
        self.ease_factor = ease_factor
        self.interval = interval
        self.prev_review_date = prev_review_date
        self.next_review_date = next_review_date
        self.review_sessions.add(review_session)
        self.save()
    
    def __str__(self):
        return self.name

class ReviewSession(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    quality = models.IntegerField(default=0)
    ease_factor = models.FloatField(default=2.5)
    time_started = models.DateTimeField(auto_now_add=True)
    time_finished = models.DateTimeField(null=True, blank=True)
    time_elapsed = models.IntegerField(default=0)
    completed = models.BooleanField(default=False)
    
    def __str__(self):
        return self.user.username + " " + self.task.name + " " + str(self.time_started) + " " + str(self.time_finished)
    
class Goal(models.Model):
    id = models.AutoField(primary_key=True)
    average_quality = models.FloatField(default=4)
    average_time_spent = models.FloatField(default=600)
    average_repetitions = models.IntegerField(default=3)
    total_added = models.IntegerField(default=5)
    date_created = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    
    def __str__(self):
        return self.user.username + " " + str(self.date_created)
