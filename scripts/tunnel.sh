#!/usr/bin/env bash

PORT=${1}

if [ -z "$PORT" ]; then
    echo Please specify port value or your bot server.
    echo
    echo For example. If your bot exposes 8080 port you should run:
    echo ./tunnel.sh 8080
    echo
    exit 1
fi

ngrok http $(docker-machine ip $(docker-machine active)):${PORT}
