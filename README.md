# webapp

Archived, no longer maintained.

Source of `problem.traeumerei.dev`: a Flask app that serves a random image or video from a folder. `/` picks one at random, `/<n>` serves the n-th file, `/submit` redirects to the upload share.

## Run

```sh
pip install -r requirements.txt
gunicorn -c gunicorn_config.py app:app
```

`MEDIA_FOLDER` at the top of `app.py` points at the directory to serve. `flake.nix` exports a NixOS module that runs it as a service.
