#!/usr/bin/env python

from flask import Flask, redirect, url_for, send_file, abort
import os
import random

app = Flask(__name__)
MEDIA_FOLDER = '/mnt/volume/nextcloud/data/hill/files/Photos/trolley/'

@app.route('/')
def serve_random_media():
    try:
        media_files = [file for file in os.listdir(MEDIA_FOLDER) if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.webp', '.mp4'))]
        if not media_files:
            abort(404, description="No media files found in the directory.")
        random_file = random.choice(media_files)
        #return redirect(url_for('serve_numbered_media', number=random_file.split(".")[0]))

        number = random_file.split(".")[0]
        file_path = None
        for ext in ['jpg', 'mp4']:
            potential_path = os.path.join(MEDIA_FOLDER, f"{number}.{ext}")
            if os.path.isfile(potential_path):
                file_path = potential_path
                break

        if not file_path:
            abort(404, description="File not found.")
        return send_file(file_path)
    except Exception as e:
        abort(500, description=str(e))

@app.route('/<int:number>')
def serve_numbered_media(number):
    try:
        file_path = None
        for ext in ['jpg', 'mp4']:
            potential_path = os.path.join(MEDIA_FOLDER, f"{number}.{ext}")
            if os.path.isfile(potential_path):
                file_path = potential_path
                break

        if not file_path:
            abort(404, description="File not found.")
        return send_file(file_path)
    except Exception as e:
        abort(500, description=str(e))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

