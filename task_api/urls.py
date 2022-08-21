from django.urls import path 
from .views import (
    TaskList,
    TaskDetail,
    TaskTypes,
    TaskListAdmin,
    TaskDetailAdmin,
    GoalDetail,
    ReviewSessionList,
    ReviewSessionUser,
    ReviewSessionDetail,
    TaskStats,
    TaskStatsAdmin,
    TaskStatsDetailAdmin,
)

urlpatterns = [
    path('task/', TaskList.as_view(), name='task-list'),
    path('task/<int:task_id>/', TaskDetail.as_view(), name='task-detail'),
    path('task-types/', TaskTypes.as_view(), name='task-types'),
    path('goal/', GoalDetail.as_view(), name='goal-detail'),
    path('review-session/<int:task_id>/', ReviewSessionList.as_view(), name='review-session-list'),
    path('review-session/', ReviewSessionUser.as_view(), name='review-session-user'),
    path('review-session/<int:task_id>/<int:review_session_id>/', ReviewSessionDetail.as_view(), name='review-session-detail'),
    path('task-stats/', TaskStats.as_view(), name='task-stats'),
    path('admin/task/<int:user_id>/', TaskListAdmin.as_view(), name='task-list-admin'),
    path('admin/task/<int:user_id>/<int:task_id>/', TaskDetailAdmin.as_view(), name='task-detail-admin'),
    path('admin/goal/<int:user_id>/', GoalDetail.as_view(), name='goal-detail-admin'),
    path('admin/task-stats/', TaskStatsAdmin.as_view(), name='task-stats-admin'),
    path('admin/task-stats/<int:user_id>/', TaskStatsDetailAdmin.as_view(), name='task-stats-detail-admin'),
]