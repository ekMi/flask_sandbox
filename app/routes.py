from app import app
import os
from flask import flash, render_template, redirect, url_for, request, send_from_directory
from app.upload_file import allowed_file
from werkzeug.utils import secure_filename


@app.route("/")
def hello():
    return "Hello World!"


@app.route('/process_request', methods=['GET', 'POST'])
def process_request():
    if request.method == 'POST':
        _name = request.form['name']
        _surname = request.form['surname']
        _birthdate = request.form['date_of_birth']
        _nationality = request.form['nationality']

        if _name:
            return render_template('process_response.html', name = _name, surname = _surname)
        else:
            return 'Please go back and enter your name', 400
    else:
        return render_template('process_form.html')


@app.route('/upload_file', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post method has file part
        if 'file' not in request.files:
            # flash 'No file part, Danger'
            return redirect(request.base_url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            # flash 'No selected file, Danger'
            return redirect(request.base_url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file', filename=filename))
    else:
        return render_template('upload_file.html')


@app.route('/uploaded_file/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    # return "file uploaded"
