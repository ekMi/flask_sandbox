from app import app
import os
from flask import flash, render_template, redirect, url_for, request, send_from_directory
from app.upload_file import allowed_file
from werkzeug.utils import secure_filename
from app.forms import My_login_form
from app.models import User
from flask_login import login_required, login_user, logout_user, current_user
# create some dummy users with ids 1 to 5
users = [User(id) for id in range(1,5)]


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route("/")
@login_required
def main():
    return render_template('index.html')


@app.route("/page_a")
@login_required
def page_a():
    return render_template('page_a.html')


@app.route("/page_b")
@login_required
def page_b():
    return render_template('page_b.html')


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main'))
    form = My_login_form()
    if form.validate_on_submit():
        user_found = False
        for n in range(0, len(users)):
            if users[n].get_name() == form.username.data:
                user_found = True
                break
        if user_found:
            if form.password.data == form.username.data + "_secret":
                id = form.username.data.split('user')[1]
                user = User(id)
                login_user(user)
                return redirect(url_for('main'))
            else:
                flash('Wrong password', 'danger')
                return redirect(url_for('login'))
        else:
            flash('User not found', 'danger')
            return redirect(url_for('login'))
    else:
        return render_template('my_login_form.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main'))


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
            flash('No file part', 'danger')
            return redirect(request.base_url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file', 'danger')
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

@app.route('/jinja2learn')
def jinja2learn():
    return render_template('jinja2learn.html', name = "Michaël")
