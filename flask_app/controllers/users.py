from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.user import User
from flask_app.models.post import Post 
from flask_bcrypt import Bcrypt
import re 
bcrypt = Bcrypt(app)

@app.route('/create', methods=['POST'])
def create_user():
    if not User.validate_user(request.form):
        return redirect('/')
    email_data = { "email" : request.form["email"] }
    user_in_db = User.get_by_email(email_data)
    if user_in_db:
        flash("That email is already being used")
        return redirect("/")
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password" : pw_hash
    }
    User.save(data)
    email_data = { "email" : request.form["email"] }
    user_in_db = User.get_by_email(email_data)
    session['user_id'] = user_in_db.id
    session.update(request.form)
    return redirect("/dashboard")

@app.route('/')
@app.route('/reg/log')
def index():
    return render_template('reg_log.html')

@app.route('/dashboard')
def show_dashboard():
    if not session:
        return redirect('/')
    session_user_id = session['user_id'] 
    return render_template('dashboard.html', posts_and_users = Post.get_all_posts_with_user(), session_user_id=session_user_id)

@app.route('/logout', methods = ['POST'])
def logout():
    session.clear()
    return redirect('/')

@app.route('/login', methods=['POST'])
def login():
    data = { "email" : request.form["email"] }
    user_in_db = User.get_by_email(data)
    if not user_in_db:
        flash("Invalid Email/Password")
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Invalid Email/Password")
        return redirect('/')
    session['user_id'] = user_in_db.id
    return redirect("/dashboard")
