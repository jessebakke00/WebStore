#! /bin/bash

RUN_DIR=`ls /var/run | grep gunicorn`

echo $RUN_DIR

if [ -z $RUN_DIR ]
then
	echo "Making Gunicorn PID Directory and changing ownership"
	sudo mkdir /var/run/gunicorn && 
	sudo chown -R jesse:jesse /var/run/gunicorn
fi

source /home/jesse/WebStore/env/bin/activate &&

cd /home/jesse/WebStore/EcomSite &&

echo "[Killing Gunicorn]"
killall gunicorn

echo "[Restarting Gunicorn]"
gunicorn -c /home/jesse/WebStore/EcomSite/conf/dev.py EcomSite.wsgi
