#!/usr/bin/env nix-shell
#! nix-shell -p python312
python -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
python setup.py install