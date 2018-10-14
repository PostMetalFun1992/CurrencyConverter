from celery_app.config import app

from converter_app.utils import upload_rates


@app.task
def task_load_rates():
    print('--- Task "load-rates" started ---')

    upload_rates()

    print('--- Task "load-rates" ended   ---')
