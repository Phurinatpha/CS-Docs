from app import db
from sqlalchemy_serializer import SerializerMixin

class order_info(db.Model, SerializerMixin):
    __tablename__ = "order_info"


    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(500))
    doc_date = db.Column(db.String(200))
    ref_num = db.Column(db.Integer)
    ref_year = db.Column(db.Integer)
    ref_name = db.Column(db.ARRAY(db.String))
    user_id = db.Column(db.Integer)

    def __init__(self, subject, doc_date, ref_num, ref_year, ref_name,user_id):
        self.subject = subject
        self.doc_date = doc_date
        self.ref_num = ref_num
        self.ref_year = ref_year
        self.ref_name = ref_name
        self.user_id = user_id



    def update(self, subject, doc_date, ref_num, ref_year, ref_name,user_id):
        self.subject = subject
        self.doc_date = doc_date
        self.ref_num = ref_num
        self.ref_year = ref_year
        self.ref_name = ref_name
        self.user_id = user_id

'''class doc_info(db.Model, SerializerMixin):
    __tablename__ = "doc"


    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(20))
    doc_data = db.Column(db.LargeBinary)

    def __init__(self, filename, doc_data):
        self.filename = filename
        self.doc_data = doc_data
    def update(self, filename, doc_data):
        self.filename = filename
        self.doc_data = doc_data'''
