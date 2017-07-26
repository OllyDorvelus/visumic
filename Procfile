web: gunicorn vidcraft.wsgi
worker: worker: celery -A vidcraft.tasks worker --loglevel=info --concurrency=1
