from datetime import timedelta

from kombu import Queue

from celery_app.config import app
from converter.enviroments import RATES_UPDATE_PERIOD_DAYS

app.conf.task_default_queue = 'default'

app.conf.task_queues = (
    Queue('default', routing_key='default.#'),
    Queue('load_rates', routing_key='load.#'),
)

app.conf.task_routes = {
    'celery_app.tasks.task_load_rates': {
        'queue': 'load_rates',
        'routing_key': 'load.load_rates',
    },
}

app.conf.beat_schedule = {
    'load-rates': {
        'task': 'celery_app.tasks.task_load_rates',
        'schedule': timedelta(days=RATES_UPDATE_PERIOD_DAYS),
        'args': (),
    },
}
