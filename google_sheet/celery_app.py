from datetime import timedelta

from celery import Celery

from config import settings

celery: Celery = Celery('sheet_parse')

celery.conf.update(
    broker_url=settings.BROKER_URL,
    result_backend='rpc://',
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],
    timezone='Europe/Moscow',
    enable_utc=True,
    beat_schedule={
        'main': {
            'task': 'google_sheet.sheet_parse.main',
            'schedule': timedelta(seconds=15),
        },
    })
