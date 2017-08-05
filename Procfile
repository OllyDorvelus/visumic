web: gunicorn vidcraft.wsgi
worker: celery -A videos.tasks worker --loglevel=info --concurrency=1

