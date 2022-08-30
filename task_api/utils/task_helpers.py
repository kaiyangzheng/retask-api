from task_api.models import ReviewSession
from datetime import datetime, timedelta
from django.utils import timezone

def get_tasks_stats(tasks):
    basic_info = {
        'total_tasks_added': tasks.count(),
        'total_tasks_with_review': tasks.filter(prev_review_date__isnull=False).count(),
        'total_repetitions': 0,
        'action_required': 0,
    }
    stats = {
        'total_understood': 0,
        'total_perfect': 0,
        'total_blackout': 0,
        'average_quality': 0,
        'average_repetitions': 0,
        'average_time_spent': 0
    }
    improvement = {
        'average_quality': {
            'current': 0,
            'prev_review': 0,
            'average_prev_reviews': 0,
        },
        'percent_understood': {
            'current': 0,
            'prev_review': 0,
            'average_prev_reviews': 0,
        },
        'average_time_spent':{
            'current': 0,
            'prev_review': 0,
            'average_prev_reviews': 0,
        },
        'average_ease_factor':{
            'current': 0,
            'prev_review': 0,
            'average_prev_reviews': 0,
        }
    }
    count = 0
    for task in tasks:
        basic_info['total_repetitions'] += task.repetitions
        if (task.prev_review_date) == None:
            basic_info['action_required'] += 1
        else: 
            if task.quality >= 3:
                stats['total_understood'] += 1
            if task.quality == 5:
                stats['total_perfect'] += 1
            if task.quality == 0:
                stats['total_blackout'] += 1
            stats['average_quality'] += task.quality
            stats['average_repetitions'] += task.repetitions
            stats['average_time_spent'] += task.review_sessions.all()[len(task.review_sessions.all()) - 1].time_elapsed

            prev_review_sessions = task.review_sessions.all()[:len(task.review_sessions.all()) - 1]
            prev_review_session = task.review_sessions.all()[len(task.review_sessions.all()) - 2] if len(task.review_sessions.all()) > 1 else None
            curr_review_session = task.review_sessions.all()[len(task.review_sessions.all()) - 1]

            improvement['average_quality']['current'] += task.quality
            improvement['average_quality']['prev_review'] += prev_review_session.quality if prev_review_session else 0
            improvement['average_quality']['average_prev_reviews'] += sum([session.quality for session in prev_review_sessions])
            improvement['average_quality']['average_prev_reviews'] /= len(prev_review_sessions) if len(prev_review_sessions) > 0 else 1

            improvement['percent_understood']['current'] += 1 if task.quality >= 3 else 0
            improvement['percent_understood']['prev_review'] += 1 if prev_review_session and prev_review_session.quality >= 3 else 0
            improvement['percent_understood']['average_prev_reviews'] = sum([1 if session.quality >= 3 else 0 for session in prev_review_sessions])
            improvement['percent_understood']['average_prev_reviews'] /= len(prev_review_sessions) if len(prev_review_sessions) > 0 else 1

            improvement['average_time_spent']['current'] += curr_review_session.time_elapsed
            improvement['average_time_spent']['prev_review'] += prev_review_session.time_elapsed if prev_review_session else 0
            improvement['average_time_spent']['average_prev_reviews'] = sum([session.time_elapsed for session in prev_review_sessions])
            improvement['average_time_spent']['average_prev_reviews'] /= len(prev_review_sessions) if len(prev_review_sessions) > 0 else 1

            improvement['average_ease_factor']['current'] += task.ease_factor
            improvement['average_ease_factor']['prev_review'] += prev_review_session.ease_factor if prev_review_session else 0
            improvement['average_ease_factor']['average_prev_reviews'] = sum([session.ease_factor for session in prev_review_sessions])
            improvement['average_ease_factor']['average_prev_reviews'] /= len(prev_review_sessions) if len(prev_review_sessions) > 0 else 1

            count += 1

    stats['average_quality'] = stats['average_quality'] / count if count > 0 else 0
    stats['average_repetitions'] = stats['average_repetitions'] / count if count > 0 else 0
    stats['average_time_spent'] = stats['average_time_spent'] / count if count > 0 else 0

    improvement['average_quality']['current'] = improvement['average_quality']['current'] / count if count > 0 else 0
    improvement['average_quality']['prev_review'] = improvement['average_quality']['prev_review'] / count if count > 0 else 0
    improvement['average_quality']['average_prev_reviews'] = improvement['average_quality']['average_prev_reviews'] / count if count > 0 else 0

    improvement['percent_understood']['current'] = improvement['percent_understood']['current'] / count if count > 0 else 0
    improvement['percent_understood']['prev_review'] = improvement['percent_understood']['prev_review'] / count if count > 0 else 0
    improvement['percent_understood']['average_prev_reviews'] = improvement['percent_understood']['average_prev_reviews'] / count if count > 0 else 0   

    improvement['average_time_spent']['current'] = improvement['average_time_spent']['current'] / count if count > 0 else 0
    improvement['average_time_spent']['prev_review'] = improvement['average_time_spent']['prev_review'] / count if count > 0 else 0
    improvement['average_time_spent']['average_prev_reviews'] = improvement['average_time_spent']['average_prev_reviews'] / count if count > 0 else 0

    improvement['average_ease_factor']['current'] = improvement['average_ease_factor']['current'] / count if count > 0 else 0
    improvement['average_ease_factor']['prev_review'] = improvement['average_ease_factor']['prev_review'] / count if count > 0 else 0
    improvement['average_ease_factor']['average_prev_reviews'] = improvement['average_ease_factor']['average_prev_reviews'] / count if count > 0 else 0

    return basic_info, stats, improvement

def get_task_types(tasks):
    task_types = {
        'waiting_for_review': [],
        'next_up': [],
        'due': [],
        'in_progress': [],
        'overdue': [],
        'all_clear': [],
    }
    now = timezone.now()
    for task in tasks:
        if task.prev_review_date == None:
            task_types['waiting_for_review'].append(task)
            return 
        review_sessions = ReviewSession.objects.filter(task=task)
        for review_session in review_sessions:
                if not review_session.completed:
                    task_types['in_progress'].append(task)
        now_date = now.date()
        next_review_date = task.next_review_date.date() 
        if next_review_date == now_date:
            task_types['due'].append(task)
        elif next_review_date < now_date:
            task_types['overdue'].append(task)
        elif next_review_date >= now_date + timedelta(days=1) and next_review_date <= now_date + timedelta(days=3):
            task_types['next_up'].append(task)
        elif next_review_date > now_date + timedelta(days=3):
            task_types['all_clear'].append(task)
    return task_types
        