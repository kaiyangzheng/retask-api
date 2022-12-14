from rest_framework import serializers
from .models import Task, ReviewSession, Goal

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'name', 'description', 'quality', 'repetitions', 'ease_factor', 'prev_review_date', 'next_review_date', 'interval', 'favorite', 'date_added', 'review_sessions', 'user')
        
class ReviewSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewSession
        fields = ('id', 'user', 'task', 'quality', 'ease_factor', 'time_started', 'time_finished', 'time_elapsed', 'completed')

class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = ('id', 'date_added', 'total_added', 'average_quality', 'average_repetitions', 'average_time_spent', 'user')
        
# class GoalSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Goal
#         fields = ('id', 'average_quality', 'average_time_spent', 'average_repetitions', 'total_added', 'date_created', 'deadline', 'user')