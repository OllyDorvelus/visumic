web: waitress-serve --port=$PORT vidcraft.wsgi:application
worker: celery worker -A vidcraft -E -l debug
chatworker: python manage.py run_chat_server


