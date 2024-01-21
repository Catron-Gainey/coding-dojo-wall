from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
import re
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask_app.models import user


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
class Post:
    db = "coding_dojo_wall" #which database are you using for this project
    def __init__(self, data):
        self.id = data['id']
        self.user_id = data['user_id']
        self.content = data['content']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user = None

    @classmethod
    def save(cls, data):
        query = """INSERT INTO posts (content, user_id)
                VALUES (%(content)s, %(user_id)s);"""
        result = connectToMySQL(cls.db).query_db(query,data)
        return result
    
    @classmethod
    def get_all_posts_with_user(cls):
        query = "SELECT * FROM posts JOIN users ON posts.user_id = users.id ORDER BY posts.updated_at Desc;"
        results = connectToMySQL('coding_dojo_wall').query_db(query)
        all_posts = []
        for row in results:
            one_post = cls(row)
            one_posts_author_info = {
                "id": row['users.id'], 
                "first_name": row['first_name'],
                "last_name": row['last_name'],
                "email": row['email'],
                "password": row['password'],
                "created_at": row['users.created_at'],
                "updated_at": row['users.updated_at']
            }
            author = user.User(one_posts_author_info)
            one_post.user = author
            all_posts.append(one_post)
        return all_posts

    @classmethod
    def delete_post(cls, id):
        query  = "DELETE FROM posts WHERE id = %(id)s;"
        result = connectToMySQL(cls.db).query_db(query, {"id":id})
        return result

    @staticmethod
    def validate_post(data):
        is_valid = True
        if len(data['content']) < 1:
            flash("content can't be less than 1 character.")
            is_valid = False
        return is_valid
