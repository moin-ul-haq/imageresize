import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'imageresize.settings')

app = Celery('myproject', broker='amqp://localhost')  # RabbitMQ as broker
app.conf.result_backend = 'redis://localhost:6379/0'  # Redis backend
app.autodiscover_tasks()