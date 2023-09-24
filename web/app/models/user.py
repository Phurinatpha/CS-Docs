from app import db
from sqlalchemy_serializer import SerializerMixin

def role_name(role):
    if role == True :
        return "ธุรการ"
    else:
        return "บุคลากร"
        
class User (db.Model, SerializerMixin):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100))
    lastname = db.Column(db.String(100))
    role = db.Column(db.Boolean)
    email = db.Column(db.String(100))


    def __init__(self, firstname, lastname,role,email):
        self.firstname = firstname
        self.lastname = lastname
        self.role = role
        self.email = email
        
    
    def update(self,role,email):
        self.role = role
        self.email = email

    def get_name(self):
        return self.firstname+" "+self.lastname
    
        
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.firstname+" "+self.lastname,
            'role': role_name(self.role),
            'email': self.email
        }