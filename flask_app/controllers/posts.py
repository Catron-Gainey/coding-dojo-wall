from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.user import User
from flask_app.models.post import Post # import entire file, rather than class, to avoid circular imports
from flask_bcrypt import Bcrypt
import re 
bcrypt = Bcrypt(app)
# As you add model files add them the the import above
# This file is the second stop in Flask's thought process, here it looks for a route that matches the request

@app.route('/create/post', methods=['POST'])
def create_post():
    if not Post.validate_post(request.form):
        return redirect('/dashboard')
    Post.save({
        **request.form,
        'user_id': session['user_id']
    })
    return redirect('/dashboard')

@app.route('/delete/<int:id>')
def remove_post(id):
    Post.delete_post(id)
    return redirect("/dashboard")