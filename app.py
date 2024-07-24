#!/usr/bin/env python

import logging
import mimetypes
import os
import random
import subprocess
import threading

import magic
from flask import Flask, abort, redirect, send_file
from PIL import Image
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
MEDIA_FOLDER = "/mnt/volume/nextcloud/data/hill/files/Photos/trolley/"
mime = magic.Magic(mime=True)


def get_media_files():
    return sorted(
        [
            file
            for file in os.listdir(MEDIA_FOLDER)
            if file
            and os.path.isfile(os.path.join(MEDIA_FOLDER, file))
            and mimetypes.guess_type(os.path.join(MEDIA_FOLDER, file))[0].startswith(
                ("video/", "image/")
            )
        ]
    )


@app.route("/")
def serve_random_media():
    random_number = random.randint(0, len(get_media_files()) - 1)
    return serve_numbered_media(random_number)


@app.route("/<int:number>")
def serve_numbered_media(number):
    media_files = get_media_files()
    if number < 0 or number >= len(media_files):
        abort(404)

    media_file = media_files[number]
    return send_file(os.path.join(MEDIA_FOLDER, media_file))


@app.route("/submit")
def submit_media():
    return redirect("https://nextcloud.traeumerei.dev/s/2RkCmriHeFG8dFF")


@app.after_request
def add_security_headers(response):
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    return response


def start_webserver():
    logger.info("Starting web server")
    app.run(host="127.0.0.1", port=8080)


class FileEventHandler(FileSystemEventHandler):
    def on_created(self, event):
        try:
            logger.info(f"New file {event.src_path} has been created.")
            mime_type = mime.from_file(event.src_path)
            if mime_type:
                new_file_number = len(get_media_files())
                file_extension = event.src_path.split(".")[-1]
                new_file_path = os.path.join(
                    MEDIA_FOLDER, f"{new_file_number}.{file_extension}"
                )
                os.rename(event.src_path, new_file_path)
                subprocess.run(["exiftool", "-all=", new_file_path], check=True)

                if mime_type.startswith("video/"):
                    self.reencode_video(new_file_path)
                if mime_type.startswith("image/"):
                    self.reencode_image(new_file_path)

                self.scan_files()

        except Exception as e:
            logger.exception(f"Error handling the new file: {e}")

    @staticmethod
    def scan_files():
        subprocess.run(
            ["nextcloud-occ", "files:scan", "--path", MEDIA_FOLDER], check=True
        )

    @staticmethod
    def reencode_video(file_path):
        try:
            temp_file = f"{file_path}.temp.mp4"
            subprocess.run(["ffmpeg", "-i", file_path, temp_file], check=True)
            os.replace(temp_file, file_path)
            logger.info(f"Video re-encoded and saved as {file_path}")
        except Exception as e:
            logger.exception(f"Error re-encoding video: {e}")

    @staticmethod
    def reencode_image(file_path):
        try:
            temp_file = f"{file_path}.temp.png"
            img = Image.open(file_path)
            img.save(temp_file, "PNG")
            os.replace(temp_file, file_path)
            logger.info(f"Image re-encoded and saved as {file_path}")
        except Exception as e:
            logger.exception(f"Error re-encoding image: {e}")


def start_observer():
    event_handler = FileEventHandler()
    observer = Observer()
    observer.schedule(event_handler, MEDIA_FOLDER, recursive=True)
    observer.start()
    logger.info("File observer started")
    try:
        while True:
            threading.Event().wait(1)
    finally:
        observer.stop()
        observer.join()


if __name__ == "__main__":
    observer_thread = threading.Thread(target=start_observer)
    observer_thread.start()

    webserver_thread = threading.Thread(target=start_webserver)
    webserver_thread.start()

    observer_thread.join()
    webserver_thread.join()
