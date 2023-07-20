#! /bin/bash

RUN_DIR=`ls /var/run | grep gunicorn`

echo $RUN_DIR

if [ -z $RUN_DIR ]
then
	echo "Making Gunicorn PID Directory and changing ownership"
	sudo mkdir /var/run/gunicorn && 
	sudo chown -R ubuntu:ubuntu /var/run/gunicorn
fi

source /home/ubuntu/WebStore/env/bin/activate &&

cd /home/ubuntu/WebStore/EcomSite &&

echo "[Killing Gunicorn]"
killall gunicorn

echo "[Restarting Gunicorn]"
gunicorn -c /home/ubuntu/WebStore/EcomSite/conf/prod.py EcomSite.wsgi
