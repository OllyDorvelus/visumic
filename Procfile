web: gunicorn vidcraft.wsgi
worker: worker: celery -A videos.tasks worker --loglevel=info --concurrency=1
