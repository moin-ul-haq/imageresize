import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'imageresize.settings')

app = Celery('imageresize', broker='amqp://localhost')  # RabbitMQ broker
app.conf.result_backend = 'redis://localhost:6379/0'

# Auto-discover tasks in installed apps
app.autodiscover_tasks()