from app import app
from flask import render_template, redirect, url_for, request

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
