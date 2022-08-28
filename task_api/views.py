from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Task, ReviewSession, Goal
from .serializers import TaskSerializer, ReviewSessionSerializer, GoalSerializer
from datetime import datetime, timedelta, timezone
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .utils.sm2 import sm2 # SM2 algorithm
from .utils.task_helpers import get_tasks_stats, get_task_types # helper functions for tasks

# Create your views here.
class TaskList(APIView):
    """
    Create or list tasks
    """ 
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TaskSerializer
    http_method_names = ['get', 'post']
    
    def get(self, request):
        tasks = Task.objects.filter(user=request.user)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'name': openapi.Schema(type=openapi.TYPE_STRING),
            'description': openapi.Schema(type=openapi.TYPE_STRING),
        })
    )
    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class TaskDetail(APIView):
    """
    Retrieve, update, or delete task instance
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TaskSerializer
    http_method_names = ['get', 'put', 'delete']
    
    def get(self, request, task_id):
        task = Task.objects.get(id=task_id, user=request.user)
        if not task:
            return Response(
                {'message': 'Task with id {} does not exist'.format(task_id)},
            )
        serializer = TaskSerializer(task)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'name': openapi.Schema(type=openapi.TYPE_STRING),
            'description': openapi.Schema(type=openapi.TYPE_STRING),
        }
    ))
    def put(self, request, task_id):
        task = Task.objects.get(id=task_id, user=request.user)
        if not task:
            return Response(
                {'message': 'Task with id {} does not exist'.format(task_id)},
            )
        serializer = TaskSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, task_id):
        task = Task.objects.get(id=task_id, user=request.user)
        if not task:
            return Response(
                {'message': 'Task with id {} does not exist'.format(task_id)},
            )
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class TaskTypes(APIView):
    """
    List all task types
    """
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get']
    
    def get(self, request):
        tasks = Task.objects.filter(user=request.user)
        task_types = get_task_types(tasks)
        return Response({
            'waiting_for_review': TaskSerializer(task_types['waiting_for_review'], many=True).data,
            'in_progress': TaskSerializer(task_types['in_progress'], many=True).data,
            'next_up': TaskSerializer(task_types['next_up'], many=True).data,
            'due': TaskSerializer(task_types['due'], many=True).data,
            'overdue': TaskSerializer(task_types['overdue'], many=True).data,
            'all_clear': TaskSerializer(task_types['all_clear'], many=True).data,
        }, status=status.HTTP_200_OK)   

    
class TaskListAdmin(APIView):
    """
    Retrieve tasks by admin
    """
    permission_classes = [permissions.IsAdminUser]
    serializer_class = TaskSerializer
    http_method_names = ['get']
    
    def get(self, request, user_id):
        tasks  = Task.objects.filter(user=user_id)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class TaskDetailAdmin(APIView):
    """
    Retrieve, update, or delete task instance by admin 
    """
    permission_classes = [permissions.IsAdminUser]
    serializer_class = TaskSerializer
    http_method_names = ['get', 'put', 'delete']
    
    def get(self, request, user_id, task_id):
        task = Task.objects.get(id=task_id, user=user_id)
        if not task: 
            return Response(
                {'message': 'Task with id {} from user {} does not exist'.format(task_id, user_id)},
            )
        serializer = TaskSerializer(task)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'name': openapi.Schema(type=openapi.TYPE_STRING),
            'description': openapi.Schema(type=openapi.TYPE_STRING),
        }
    ))
    def put(self, request, user_id, task_id):
        task = Task.objects.get(id=task_id, user=user_id)
        if not task:
            return Response(
                {'message': 'Task with id {} from user {} does not exist'.format(task_id, user_id)},
            )
        serializer = TaskSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, user_id, task_id):
        task = Task.objects.get(id=task_id, user=user_id)
        if not task:
            return Response(
                {'message': 'Task with id {} from user {} does not exist'.format(task_id, user_id)},
            )
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class GoalDetail(APIView):
    """
    Retrieve or create goal instance
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalSerializer
    http_method_names = ['get', 'post']
    
    def get(self, request):
        goal = Goal.objects.get(user=request.user)
        if not goal:
            return Response(
                {'message': 'Goal does not exist'},
            )
        serializer = GoalSerializer(goal)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'average_quality': openapi.Schema(type=openapi.TYPE_NUMBER),
            'average_time_spent': openapi.Schema(type=openapi.TYPE_NUMBER),
            'average_repetitions': openapi.Schema(type=openapi.TYPE_NUMBER),
            'total_added': openapi.Schema(type=openapi.TYPE_NUMBER),
            'date_created': openapi.Schema(type=openapi.TYPE_STRING),
            'deadline': openapi.Schema(type=openapi.TYPE_STRING),
        }
    ))
    def post(self, request):
        self.delete(request)
        serializer = GoalSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request):
        goal = Goal.objects.get(user=request.user)
        goal.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class GoalDetailAdmin(APIView):
    """
    Retrieve or delete goal instance by admin 
    """
    permission_classes = [permissions.IsAdminUser] 
    serializer_class = GoalSerializer
    htp_method_names = ['get', 'delete']
    
    def get(self, request, user_id):
        goal = Goal.objects.get(user=user_id)
        if not goal:
            return Response(
                {'message': 'Goal for user {} does not exist'.format(user_id)},
            )
        serializer = GoalSerializer(goal)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, user_id):
        goal = Goal.objects.get(user=user_id)
        if not goal:
            return Response(
                {'message': 'Goal for user {} does not exist'.format(user_id)},
            )
        goal.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class ReviewSessionList(APIView):
    """
    Retrieve and create review sessions 
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, task_id):
        review_sessions = ReviewSession.objects.filter(task=task_id, user=request.user)
        if not review_sessions:
            return Response(
                {'message': 'Review sessions for task {} do not exist'.format(task_id)},
            )
        serializer = ReviewSessionSerializer(review_sessions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, task_id):
        task = Task.objects.get(id=task_id)
        if not task:
            return Response(
                {'message': 'Task with id {} does not exist'.format(task_id)},
            )
        data = {
            'user': request.user.id,
            'task': task_id
        }
        serializer = ReviewSessionSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReviewSessionUser(APIView):
    """
    Retrieve all review sessions by user
    """
    def get(self, request):
        review_sessions = ReviewSession.objects.filter(user=request.user)
        if not review_sessions:
            return Response(
                {'message': 'Review sessions for user {} do not exist'.format(request.user.id)},
            )
        serializer = ReviewSessionSerializer(review_sessions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ReviewSessionDetail(APIView):
    """
    Retrieve, update/finish, or delete review session
    """
    def get(self, request, task_id, review_session_id):
        review_session = ReviewSession.objects.get(id=review_session_id, task=task_id)
        if not review_session:
            return Response(
                {'message': 'Review session with id {} for task {} does not exist'.format(review_session_id, task_id)},
            )
        serializer = ReviewSessionSerializer(review_session)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'quality': openapi.Schema(type=openapi.TYPE_NUMBER),
        }
    ))
    def put(self, request, task_id, review_session_id):
        task = Task.objects.get(id=task_id)
        review_session = ReviewSession.objects.get(id=review_session_id, task=task_id)
        if not task or not review_session:
            return Response(
                {'message': 'Review session with id {} for task {} does not exist'.format(review_session_id, task_id)},
            )
        today = datetime.now(timezone.utc)
        data = {
            'user': request.user.id,
            'task': task_id,
            'quality': request.data.get('quality'),
            'time_finished': today,
            'time_elapsed': int((today - review_session.time_started).total_seconds()),
            'completed': True
        }
        new_interval, new_repetitions, new_ease_factor = sm2(data['quality'], task.repetitions, task.ease_factor, task.interval)
        new_task_data = {
            'repetitions': new_repetitions,
            'next_review_date': today + timedelta(days=new_interval),
            'prev_review_date': today,
            'interval': new_interval,
            'ease_factor': new_ease_factor,
            'quality': data['quality'],
            'review_session': review_session
        }
        task.update(**new_task_data)
        serializer = ReviewSessionSerializer(review_session, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, task_id, review_session_id):
        review_session = ReviewSession.objects.get(id=review_session_id, task=task_id)
        if not review_session:
            return Response(
                {'message': 'Review session with id {} for task {} does not exist'.format(review_session_id, task_id)},
            )
        review_session.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class TaskStats(APIView):
    """
    Retrieve task stats
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        tasks = Task.objects.filter(user=request.user)
        if not tasks:
            return Response(
                {'message': 'Tasks for user {} do not exist'.format(request.user.id)},
            )
        basic_info, stats, improvement = get_tasks_stats(tasks)
        return Response({
            'basic_info': basic_info,
            'stats': stats,
            'improvement': improvement
        }, status=status.HTTP_200_OK)

class TaskStatsAdmin(APIView):
    """
    Retrieve task stats for all users by admin
    """
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        tasks = Task.objects.all()
        if not tasks:
            return Response(
                {'message': 'Tasks do not exist'},
            )
        basic_info, stats, improvement = get_tasks_stats(tasks)
        return Response({
            'basic_info': basic_info,
            'stats': stats,
            'improvement': improvement
        }, status=status.HTTP_200_OK)

class TaskStatsDetailAdmin(APIView):
    """ 
    Retrieve task stats for specific user by admin
    """
    permission_classes = [permissions.IsAdminUser]

    def get(self, request, user_id):
        tasks = Task.objects.filter(user=user_id)
        if not tasks:
            return Response(
                {'message': 'Tasks for user {} do not exist'.format(user_id)},
            )
        basic_info, stats, improvement = get_tasks_stats(tasks)
        return Response({
            'basic_info': basic_info,
            'stats': stats,
            'improvement': improvement
        }, status=status.HTTP_200_OK)
