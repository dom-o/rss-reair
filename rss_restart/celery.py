import os
from celery import Celery
from celery.schedules import crontab

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rss_restart.settings.base')

app= Celery('rss_restart')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    # 'test-task': {
    #     'task': 'rss.tasks.test_task',
    #     'schedule': 10.0,
    #     'args': (),
    # },
    'publish-daily': {
        'task': 'rss.tasks.publish',
        'schedule': crontab(minute=0, hour=0),
        'args': (),
    },
    'clear-old-feeds-daily': {
        'task': 'rss.tasks.clear_old_feeds',
        'schedule': crontab(minute=0, hour=0),
        'args': ()
    }
}

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
