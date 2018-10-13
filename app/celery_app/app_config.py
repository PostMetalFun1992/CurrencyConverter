from datetime import timedelta
import os

from celery import Celery
from kombu import Queue

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'converter.settings')

RATES_UPDATE_PERIOD_DAYS = int(os.getenv('RATES_UPDATE_PERIOD_DAYS', '1'))

RABBITMQ_DEFAULT_USER = os.getenv('RABBITMQ_DEFAULT_USER', '')
RABBITMQ_DEFAULT_PASS = os.getenv('RABBITMQ_DEFAULT_PASS', '')
RABBITMQ_DEFAULT_VHOST = os.getenv('RABBITMQ_DEFAULT_VHOST', '')

RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', '')
RABBITMQ_PORT = os.getenv('RABBITMQ_PORT', '')

REDIS_HOST = os.getenv('REDIS_HOST', '')
REDIS_PORT = os.getenv('REDIS_PORT', '')

app = Celery('converter')

broker_url = 'amqp://{user}:{passw}@{host}:{port}/{vhost}'.format(
    user=RABBITMQ_DEFAULT_USER,
    passw=RABBITMQ_DEFAULT_PASS,
    host=RABBITMQ_HOST,
    port=RABBITMQ_PORT,
    vhost=RABBITMQ_DEFAULT_VHOST,
)

result_backend = 'redis://{host}:{port}'.format(
    host=REDIS_HOST,
    port=REDIS_PORT,
)

app.conf.update(
    broker_url=broker_url,
    result_backend=result_backend,
    imports=['converter_app.utils']
)

app.conf.task_default_queue = 'default'

app.conf.task_queues = (
    Queue('default', routing_key='default.#'),
    Queue('load_rates', routing_key='load.#'),
)

app.conf.task_routes = {
    'converter_app.utils.load_rates': {
        'queue': 'load_rates',
        'routing_key': 'load.load_rates',
    },
}

app.conf.beat_schedule = {
    'load-rates': {
        'task': 'converter_app.utils.load_rates',
        'schedule': timedelta(days=RATES_UPDATE_PERIOD_DAYS),
        'args': (),
    },
}
