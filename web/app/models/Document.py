from app import db
from sqlalchemy_serializer import SerializerMixin

class Document(db.Model, SerializerMixin):
    __tablename__ = "document"


    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(500))
    doc_path = db.Column(db.LargeBinary)
    doc_date = db.Column(db.String(300))
    doc_num = db.Column(db.String(20))
    ref_name = db.Column(db.ARRAY(db.String))
    user_id = db.Column(db.Integer)

    def __init__(self, subject, doc_path, doc_date, doc_num,ref_name,user_id):
        self.subject = subject
        self.doc_path = doc_path
        self.doc_date = doc_date
        self.doc_num = doc_num
        self.ref_name = ref_name
        self.user_id = user_id



    def update(self, subject, doc_path, doc_date, doc_num,ref_name,user_id):
        self.subject = subject
        self.doc_path = doc_path
        self.doc_date = doc_date
        self.doc_num = doc_num
        self.ref_name = ref_name
        self.user_id = user_id