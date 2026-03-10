from .celery import app as celery_app

__all__ = ('celery_app',)

# This makes the Celery app importable as 'imageresize.app'
app = celery_app