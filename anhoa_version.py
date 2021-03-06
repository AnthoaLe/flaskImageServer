from rembg.bg import remove
import numpy as np
import io
import time
from PIL import Image
from flask import Flask, flash, redirect, request, send_from_directory, send_file, url_for

import os

# Add these lines for bigger images
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

app = Flask(__name__)   # Pass the name of the package

UPLOAD_FOLDER = "upload_images"   # Global variable, where images I want to upload are stored
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'} # Global variable of file extensions that are allowed to be uploaded
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER # Configure a folder of images we wish to upload

@app.route('/helloworld')
def hello_word():
    return "Hello World"

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[-1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods= ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Checks POST has a file key
        if 'file' not in request.files:
            flash('No file key')
            return redirect(request.url)

        # Checks POST has a file uploaded
        file = request.files['file']
        if file.filename == '':
            flash('No file uploaded')
            return redirect(request.url)

        # If file exists and is an acceptable file type
        # Specified by ALLOWED_EXTENSIONS
        if file and allowed_file(file.filename):
            filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filename)

            input_path = filename
            output_path = 'image-' + str(int(time.time())) + '.png' # Must be a .png

            file = np.fromfile(input_path)
            result = remove(file)
            img = Image.open(io.BytesIO(result)).convert('RGBA')
            img.save(output_path)

            return redirect(url_for('uploaded_file', filename=output_path))

    return '''
        <!doctype html>
        <title>Upload new File</title>
        <h1>Upload new File</h1>
        <form method=post enctype=multipart/form-data>
          <input type=file name=file>
          <input type=submit value=Upload>
        </form>
        '''

@app.route('/uploads/<filename>')   # <filename> template for actual filename
def uploaded_file(filename):
    return send_from_directory('', filename)

app.run(host= "0.0.0.0")    # Runs the Flask server on local host