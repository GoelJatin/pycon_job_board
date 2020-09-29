release: python manage.py migrate
web: gunicorn job_board.wsgi -w 10 --log-file -
