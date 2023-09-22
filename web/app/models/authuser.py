from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin
from app import db

class AuthUser(db.Model, UserMixin):
    __tablename__ = "auth_users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(500))
    

    def __init__(self, email, password):
        self.email = email
        self.password = password
        

    def update(self, email, name):
        self.email = email
        self.name = name
        