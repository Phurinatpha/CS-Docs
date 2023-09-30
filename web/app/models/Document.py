from app import db
from sqlalchemy_serializer import SerializerMixin
from app.models.user import User

def to_date(date):
    month_name = 'x มกราคม กุมภาพันธ์ มีนาคม เมษายน พฤษภาคม มิถุนายน กรกฎาคม สิงหาคม กันยายน ตุลาคม พฤศจิกายน ธันวาคม'.split()[date.month]
    thai_year = date.year 
    return "%d %s %d"%(date.day, month_name, thai_year) # 30 ตุลาคม 2560 20:45:30

def to_ori_date(date):
    month_name = 'x 1 2 3 4 5 6 7 8 9 10 11 12'.split()[date.month]
    thai_year = date.year 
    return "%d/%s/%d"%(date.day, month_name, thai_year)


class order_info(db.Model, SerializerMixin):
    __tablename__ = "order_info"


    #id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(500))
    doc_date = db.Column(db.Date)
    ref_num = db.Column(db.Integer)
    ref_year = db.Column(db.Integer)
    ref_name = db.Column(db.ARRAY(db.String))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    __table_args__ = (
    db.PrimaryKeyConstraint(
        "ref_num", "ref_year",name="pk_id"
        ),
    )

    def __init__(self, subject, doc_date, ref_num, ref_year, ref_name,user_id):
        self.subject = subject
        self.doc_date = doc_date
        self.ref_num = ref_num
        self.ref_year = ref_year
        self.ref_name = ref_name
        self.user_id = user_id



    def update(self, subject, doc_date,   ref_name,user_id):
        self.subject = subject
        self.doc_date = doc_date
        self.ref_name = ref_name
        self.user_id = user_id

    def mini_update(self, subject):
        self.subject = subject
    
    def to_dict(self):
        return {
            #'id': self.pk_id,
            'ref_num': str(self.ref_num)+"/"+str(self.ref_year),
            'subject': self.subject,
            'doc_date': to_date(self.doc_date),
            'ori_date':to_ori_date(self.doc_date),
            'ref_name': ','.join([str(elem) for elem in self.ref_name]),

            'user_name' : User.get_name(User.query.get(self.user_id))
        }
class doc_info(db.Model, SerializerMixin):
    __tablename__ = "doc_info"


    id = db.Column(db.Integer, primary_key=True)
    order_refnum = db.Column(db.Integer)
    order_refyear = db.Column(db.Integer)
    filename = db.Column(db.String(20))
    doc_data = db.Column(db.LargeBinary)
    __table_args__ = (
        db.ForeignKeyConstraint(
             ['order_refnum', 'order_refyear'],
            ['order_info.ref_num', 'order_info.ref_year'],
        ),
)

    def __init__(self, order_refnum, order_refyear, filename, doc_data):
        self.order_refnum = order_refnum
        self.order_refyear = order_refyear
        self.filename = filename
        self.doc_data = doc_data
    def update(self,  doc_data):
        self.doc_data = doc_data
    
    def to_dict(self):
        return {
            'id': self.id,
            'order_id': str(self.order_refnum)+" "+str(self.order_refyear),
            'filename': self.filename
        }
