from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
import re
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask_app.models import user

class Comment:
    db = "coding_dojo_wall" 
    def __init__(self, data):
        self.id = data['id']
        self.user_id = data['user_id']
        self.post_id = data['post_id']
        self.content = data['content']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user = None


    @classmethod
    def save(cls, data):
        query = """INSERT INTO comments (content, user_id, post_id)
                VALUES (%(content)s, %(user_id)s, %(post_id)s);"""
        result = connectToMySQL(cls.db).query_db(query,data)
        return result