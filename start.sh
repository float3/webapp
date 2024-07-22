#!/usr/bin/env nix-shell
#! nix-shell -p python312Packages.gunicorn
gunicorn -c gunicorn_config.py app:app
