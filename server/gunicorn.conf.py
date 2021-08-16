#!/usr/bin/env python3

from os import getenv
import multiprocessing

# Set default values
# ---------------------

WEB_CONCURRENCY = getenv('GUNICORN_WEB_CONCURRENCY', None)
HOST = getenv('GUNICORN_HOST', '0.0.0.0')
PORT = getenv('GUNICORN_PORT', '8080')
BIND = getenv('GUNICORN_BIND', None)
LOG_LEVEL = getenv('GUNICORN_LOG_LEVEL', 'info')
KEEPALIVE = int(getenv('GUNICORN_KEEPALIVE', '4'))

# Set Gunicorn config variables
# ---------------------

# https://docs.gunicorn.org/en/stable/settings.html#loglevel
loglevel = getenv('GUNICORN_LOG_LEVEL', 'info')

# https://docs.gunicorn.org/en/stable/settings.html#accesslog
accesslog = '-'

# https://docs.gunicorn.org/en/stable/settings.html#errorlog
errorlog = '-'

# https://docs.gunicorn.org/en/stable/settings.html#bind
bind = BIND if BIND else f'{HOST}:{PORT}'

# https://docs.gunicorn.org/en/stable/settings.html#workers
# https://docs.gunicorn.org/en/stable/design.html#how-many-workers
num_cores = multiprocessing.cpu_count()
workers = min(WEB_CONCURRENCY if WEB_CONCURRENCY else (2 * num_cores) + 1, 12)

# https://docs.gunicorn.org/en/stable/settings.html#worker-class
worker_class = 'sync'

# https://docs.gunicorn.org/en/stable/settings.html#keepalive
keepalive = KEEPALIVE

# https://docs.gunicorn.org/en/stable/settings.html#preload-app
preload = True
