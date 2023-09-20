from flask.cli import FlaskGroup
from werkzeug.security import generate_password_hash
from app import app, db
from app.models.Document import order_info
from app.models.user import User
from app.models.authuser import AuthUser
#from app.models.authuser import AuthUser, PrivateContact

cli = FlaskGroup(app)


@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command("seed_db")
def seed_db():
    db.session.add(AuthUser(email='flask@1234', password=generate_password_hash('password', method='scrypt')))
    db.session.add(AuthUser(email='ksalf@4321', password=generate_password_hash('password', method='scrypt'))) 
    db.session.add(User(firstname='สมชาย',lastname="ทรงแบด",role='admin',email="flask@1234"))
    db.session.add(User(firstname='น้องแคท',lastname="แซดบ๋อย",role='admin',email="ksalf@4321"))
    db.session.commit()
    count = 1
    i = 1
    while count < 50 :
        db.session.add(
            order_info(subject='ฮัลโหลนี่คือข้อมูลจาก database จะขึ้นไหมน้าา', doc_date='2 กันยายน 2023',ref_num=i,ref_year='2566',ref_name=['Mr. Compsci ChiangMai University'],user_id='1'))
        db.session.add(
            order_info(subject='จริงๆแล้วฉันหนะ คือประธานบริษัทก่อสร้าง', doc_date='4 มีนาคม 2023',ref_num=i+1,ref_year='2566',ref_name=['นาย นึกว่ายาม หัวหน้านี่หว่า'],user_id='2'))
        db.session.add(
            order_info(subject='คิดจะพัก คิดถึงคิดแคท', doc_date='5 พฤศจิกายน 2023',ref_num=i+2,ref_year='2566',ref_name=['นาย คิทแคท หวานเจี้ยบ'],user_id='1'))
        db.session.add(
            order_info(subject='คิดสิ คิดสิ คาปูชิโน่วว เอสเปรสโซ่วว อาราบิก๊าา', doc_date='8 เมษายน 2023',ref_num=i+3,ref_year='2566',ref_name=['นายกาแฟดํา เพิ่มชอต','นาย โอเค หรือไม่'],user_id='2'))
    # db.session.add(PrivateContact(firstname='ส้มโอ', lastname='โอเค',phone='081-111-1112', owner_id=1))
        count += 1
        i+=4
    db.session.commit()



if __name__ == "__main__":
    cli()
