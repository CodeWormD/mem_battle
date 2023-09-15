import os

from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mem_battle.settings')

app = Celery('mem_battle', broker_url='redis://127.0.0.1:6379/0')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.broker_url = settings.CELERY_BROKER_URL
app.autodiscover_tasks()


@app.task()
def debug_task(self):
    print(f'Hello world')

# установить redis вручную (и редис сервер)
# проверить установлен ли он с селери сразу и подключить