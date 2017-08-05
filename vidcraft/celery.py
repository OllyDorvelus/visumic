from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# set the default Django settings module for the 'celery' program.
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vidcraft.settings')
#
# app = Celery('vidcraft')
# # Using a string here means the worker don't have to serialize
# # the configuration object to child processes.
# # - namespace='CELERY' means all celery-related configuration keys
# #   should have a `CELERY_` prefix.
# app.config_from_object('django.conf:settings', namespace='CELERY')
#
# # Load task modules from all registered Django app configs.
# app.autodiscover_tasks()
#
#
# @app.task(bind=True)
# def debug_task(self):
#     print('Request: {0!r}'.format(self.request))
# CEL 3.1
app = Celery('vidcraft')
@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


from django.conf import settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vidcraft.settings')
# DEFAULT_AMQP = "amqp://guest:guest@localhost//"
# DEFAULT_DB = "postgres://localhost"
# db_url = os.environ.get("DATABASE_URL", DEFAULT_DB)
# set the default Django settings module for the 'celery' program.
#app = Celery()
app = Celery('vidcraft')
# app = Celery("tasks", backend=db_url.replace("postgres://", "db+postgresql://"),
#              broker=os.environ.get("CLOUDAMQP_URL", DEFAULT_AMQP))
# app.BROKER_POOL_LIMIT = 1
# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))