from app import db
from sqlalchemy_serializer import SerializerMixin
from flask_login import UserMixin

def role_name(role):
    if role == True:
        return "ธุรการ"
    else:
        return "บุคลากร"

class User(db.Model, UserMixin):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100))
    lastname = db.Column(db.String(100))
    role = db.Column(db.Boolean)
    email = db.Column(db.String(100))

    def __init__(self, firstname, lastname, role, email):
        self.firstname = firstname
        self.lastname = lastname
        self.role = role
        self.email = email

    def update(self, role, email):
        self.role = role
        self.email = email
        
    def update_name(self, firstname, lastname):
        self.firstname = firstname
        self.lastname = lastname

    def get_name(self):
        return self.firstname + " " + self.lastname

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.firstname + " " + self.lastname,
            'role': role_name(self.role),
            'email': self.email
        }
    
    def is_active(self):
        # Return True if the user account is active, or False if it's disabled
        return True  # Modify this based on your application's logic

    def get(user_id):
            return User.query.get(user_id)