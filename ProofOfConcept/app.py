import sys
import os
import re
import os

from flask import Flask, flash, request, redirect, render_template, send_from_directory, current_app
from werkzeug.utils import secure_filename
from config import *

app = Flask(__name__)
app.secret_key = app_key

if not os.path.isdir(upload_dest):
    os.mkdir(upload_dest)

app.config['MAX_CONTENT_LENGTH'] = file_mb_max * 1024 * 1024
app.config['UPLOAD_FOLDER'] = upload_dest


@app.context_processor
def utility_processor():
    def get_files_from_upload_folder():
        path = os.path.join(current_app.root_path, app.config['UPLOAD_FOLDER'])
        only_files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
        return only_files

    def get_file_basename(path):
        return os.path.basename(path)
    return {
        'get_files_from_upload_folder': get_files_from_upload_folder,
        'get_file_basename': get_file_basename
    }


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in extensions


@app.route('/download/<path:filename>', methods=['GET', 'POST'])
def download_file(filename):
    download_folder = os.path.join(current_app.root_path, app.config['UPLOAD_FOLDER'])
    return send_from_directory(directory=download_folder, filename=filename)


@app.route('/download')
def download_form():
    return render_template('download.html')


@app.route('/upload')
def upload_form():
    return render_template('upload.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        if 'files[]' not in request.files:
            flash('No files found, try again.')
            return redirect(request.url)

        files = request.files.getlist('files[]')
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                file.close()
                flash('{} uploaded'.format(filename))
    return redirect('/upload')
  

if __name__ == "__main__":
    print('To upload files navigate to http://127.0.0.1:4000/upload')
    print('To download files navigate to http://127.0.0.1:4000/download')
    app.run(host='0.0.0.0', port=4000, debug=True, threaded=True)
