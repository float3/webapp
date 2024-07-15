#!/usr/bin/env python

import os
import random
import threading

import ffmpeg
import pyexiftool
from flask import Flask, abort, send_file
from PIL import Image
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

app = Flask(__name__)
MEDIA_FOLDER = "/mnt/volume/nextcloud/data/hill/files/Photos/trolley/"


@app.route("/")
def serve_random_media():
    try:
        media_files = [
            file
            for file in os.listdir(MEDIA_FOLDER)
            if file.lower().endswith(
                (".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tiff", ".webp", ".mp4")
            )
        ]
        if not media_files:
            abort(404, description="No media files found in the directory.")
        random_file = random.choice(media_files)
        # return redirect(url_for('serve_numbered_media', number=random_file.split(".")[0]))

        number = random_file.split(".")[0]
        file_path = None
        for ext in ["jpg", "mp4"]:
            potential_path = os.path.join(MEDIA_FOLDER, f"{number}.{ext}")
            if os.path.isfile(potential_path):
                file_path = potential_path
                break

        if not file_path:
            abort(404, description="File not found.")
        return send_file(file_path)
    except Exception as e:
        abort(500, description=str(e))


@app.route("/<int:number>")
def serve_numbered_media(number):
    try:
        file_path = None
        for ext in ["jpg", "mp4"]:
            potential_path = os.path.join(MEDIA_FOLDER, f"{number}.{ext}")
            if os.path.isfile(potential_path):
                file_path = potential_path
                break

        if not file_path:
            abort(404, description="File not found.")
        return send_file(file_path)
    except Exception as e:
        abort(500, description=str(e))


def start_webserver():
    app.run(host="0.0.0.0", port=8080)


class FileEventHandler(FileSystemEventHandler):
    def on_created(self, event):
        try:
            print(f"New file {event.src_path} has been created.")
            new_file_number = (
                max(
                    [
                        int(file.split(".")[0])
                        for file in os.listdir(MEDIA_FOLDER)
                        if file.lower().endswith((".jpg", ".mp4"))
                        and file != os.path.basename(event.src_path)
                    ]
                )
                + 1
            )

            new_file_path = os.path.join(
                MEDIA_FOLDER, f"{new_file_number}.{event.src_path.split('.')[-1]}"
            )
            os.rename(event.src_path, new_file_path)

            # Remove metadata
            with pyexiftool.ExifTool() as et:
                et.execute("-all=", new_file_path)

            # Re-encode file
            if new_file_path.lower().endswith(".mp4"):
                self.reencode_video(new_file_path)
            elif new_file_path.lower().endswith(".jpg"):
                self.reencode_image(new_file_path)

        except Exception as e:
            print(f"Error handling the new file: {e}")

    def reencode_video(self, file_path):
        try:
            temp_file = f"{file_path}.temp.mp4"
            ffmpeg.input(file_path).output(temp_file).run(overwrite_output=True)
            os.replace(temp_file, file_path)
            print(f"Video re-encoded and saved as {file_path}")
        except Exception as e:
            print(f"Error re-encoding video: {e}")

    def reencode_image(self, file_path):
        try:
            img = Image.open(file_path)
            img.save(file_path, "JPEG")
            print(f"Image re-encoded and saved as {file_path}")
        except Exception as e:
            print(f"Error re-encoding image: {e}")


def start_observer():
    event_handler = FileEventHandler()
    observer = Observer()
    observer.schedule(event_handler, MEDIA_FOLDER, recursive=False)
    observer.start()
    try:
        while True:
            # Keep the thread alive
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
