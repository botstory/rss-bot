#!/usr/bin/env bash

export PROJECT_NAME=rssbot
export PYTHONPATH=${PYTHONPATH}:$(pwd)

echo "PYTHONPATH"
echo ${PYTHONPATH}

echo "====================================================="
echo ""
echo " Setup"
echo ""
echo "====================================================="

python ./${PROJECT_NAME}/main.py --setup

echo "====================================================="
echo ""
echo " Start"
echo ""
echo "====================================================="

gunicorn ${PROJECT_NAME}.wsgi:app --bind 0.0.0.0:${PORT} --log-file - --reload --worker-class aiohttp.worker.GunicornWebWorker
