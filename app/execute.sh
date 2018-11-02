#!/usr/bin/env bash

python /app/deploy_flask.py

sleep 1

python /app/app.py
