from app import db
from sqlalchemy_serializer import SerializerMixin
from flask_login import UserMixin

def is_admin_name(is_admin):
    if is_admin == True:
        return "ธุรการ"
    else:
        return "บุคลากร"
def user_name(firstname, lastname):
    if  firstname!= "":
        return firstname +" "+ lastname
    else:
        return "ผู้ใช้งานยังไม่ได้เข้าสู่ระบบ"
class User(db.Model, UserMixin):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100))
    lastname = db.Column(db.String(100))
    is_admin = db.Column(db.Boolean, default=False)
    email = db.Column(db.String(100), unique=True)

    def __init__(self, firstname, lastname, is_admin, email):
        self.firstname = firstname
        self.lastname = lastname
        self.is_admin = is_admin
        self.email = email

    def update(self, is_admin, email):
        self.is_admin = is_admin
        self.email = email
    def update_is_admin(self, is_admin):
        self.is_admin = is_admin

    def update_name(self, firstname, lastname):
        self.firstname = firstname
        self.lastname = lastname

    def get_name(self):
        return self.firstname + " " + self.lastname

    def to_dict(self):
        return {
            'id': self.id,
            'name': user_name(self.firstname, self.lastname),
            'is_admin' : self.is_admin,
            'str_is_admin': is_admin_name(self.is_admin),
            'email': self.email
        }
    
    def is_active(self):
        # Return True if the user account is active, or False if it's disabled
        return True  # Modify this based on your application's logic

    def get(user_id):
            return User.query.get(user_id)