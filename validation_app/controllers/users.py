from validation_app import app
from validation_app.models.user import User
from validation_app.models.user import bcrypt
from flask import render_template, request, redirect, session


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/users/register', methods=['POST'])
def register():
    if not User.validate_registration(request.form):
        return redirect('/')
    else:
        pw_hash = bcrypt.generate_password_hash(request.form['password'])
        data = {
            'first_name': request.form['first_name'],
            'last_name': request.form['last_name'],
            'email': request.form['email'],
            'password': pw_hash,
        }
        user_id = User.save(data)
        session['user_id'] = user_id
        print("***********************************")
        return redirect('/users/success')


@app.route('/users/login', methods=["POST", "GET"])
def user_login():
    if 'user_id' in session:
        return redirect('/users/success')
    elif request.method == "POST":
        data = {
            'email': request.form['email'],
            'password': request.form['password']
        }
        if not User.validate_login(data):
            return redirect('/users/login')
        else:
            user = User.get_by_email(data)
            session['user_id'] = user.id
            print("this is users login")
            return redirect('/users/success')
    return render_template("login.html")


@app.route('/users/logout')
def user_logout():
    session.clear()
    return redirect('/users/login')


@app.route('/users/success')
def user_success():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id': session['user_id']
    }
    user = User.get_by_id(data)
    return render_template('success.html', user=user)
