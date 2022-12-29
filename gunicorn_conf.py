from multiprocessing import cpu_count

# Socket Path
bind = 'unix:/home/flowimpact/flowimpact_core/gunicorn.sock'

# Worker Options
workers = cpu_count() + 1
worker_class = 'uvicorn.workers.UvicornWorker'

# Logging Options
loglevel = 'debug'
accesslog = '/home/flowimpact/flowimpact_core/access_log'
errorlog =  '/home/flowimpact/flowimpact_core/error_log'
