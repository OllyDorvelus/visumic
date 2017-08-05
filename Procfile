web: gunicorn vidcraft.wsgi
worker: REMAP_SIGTERM=SIGQUIT celery -A vidcraft worker -l info


