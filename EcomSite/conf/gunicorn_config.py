command = '/home/jesse/WebStore/EcomSite/env/bin/gunicorn'
pythonpath = '/home/jesse/WebStore/EcomSite'
bind = '0.0.0.0:8001'
workers = 3
reload = True
accesslog = errorlog = "/var/log/gunicorn/ecom_dev.log"
timeout = 3600
