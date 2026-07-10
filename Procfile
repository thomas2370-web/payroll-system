web: gunicorn config.wsgi:application
release: python manage.py migrate && python manage.py collectstatic --noinput && python manage.py seed_demo_data
