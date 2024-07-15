#!/usr/bin/env sh
./venv/bin/gunicorn -c gunicorn_config.py app:app
