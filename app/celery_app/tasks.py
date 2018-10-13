from celery_app.config import app

from converter_app.utils import load_rates


@app.task
def task_load_rates():
    print('--- Task "load-rates" started ---')

    load_rates()

    print('--- Task "load-rates" ended   ---')
