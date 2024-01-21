from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.user import User
from flask_app.models.post import Post 
from flask_app.models.comment import Comment
from flask_bcrypt import Bcrypt
import re 
bcrypt = Bcrypt(app)

@app.route('/create/comment/<int:post_id>', methods=['POST'])
def create_comment(post_id):
    Comment.save({
        **request.form,
        'user_id': session['user_id'],
        'post_id': post_id
    })
    return redirect('/dashboard')