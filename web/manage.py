from flask.cli import FlaskGroup
from werkzeug.security import generate_password_hash
from app import app, db
from app.models.Document import Document
#from app.models.blogentry import BlogEntry
#from app.models.authuser import AuthUser, PrivateContact

cli = FlaskGroup(app)


@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command("seed_db")
def seed_db():

    db.session.add(
        Document(subject='ฮัลโหลนี่คือข้อมูลจาก database จะขึ้นไหมน้าา', doc_path='d/ss', doc_date='32 ก.ค. 2566',ref_num='99/2566',ref_name='Mr. Compsci ChiangMai University',user_id='1'))
    db.session.add(
        Document(subject='จริงๆแล้วฉันหนะ คือประธานบริษัทก่อสร้าง', doc_path='d/ss', doc_date='33 ก.ค. 2566',ref_num='99/2566',ref_name='นาย นึกว่ายาม หัวหน้านี่หว่า',user_id='1'))
    db.session.add(
        Document(subject='คิดจะพัก คิดถึงคิดแคท', doc_path='d/ss', doc_date='34 ก.ค. 2566',ref_num='99/2566',ref_name='นาย คิทแคท หวานเจี้ยบ',user_id='1'))
    db.session.add(
        Document(subject='คิดสิ คิดสิ คาปูชิโน่วว เอสเปรสโซ่วว อาราบิก๊าา', doc_path='d/ss', doc_date='35 ก.ค. 2566',ref_num='99/2566',ref_name='นายกาแฟดํา เพิ่มชอต',user_id='1'))
    # db.session.add(BlogEntry(name='Moosu',message='test-tw-db',email="moosu@gmu.ac.th", ref_num=''))
    #db.session.add(AuthUser(email="flask@204212" name='สมชาย ทรงแบด',password=generate_password_hash('1234',method='sha256'),avatar_url='https://ui-avatars.com/api/?name=สมชาย+ทรงแบด&background=83ee03&color=fff'))
    #db.session.add(AuthUser(email="locket@204212", name='locket',password=generate_password_hash('1234',method='sha256'),avatar_url='https://ui-avatars.com/api/?name=locket&background=83ee03&color=fff'))
    # db.session.add(BlogEntry(name='สมชาย ทรงแบด',message='test-tw-db',email="flask@204212", avatar_url='https://ui-avatars.com/api/?name=สมชาย+ทรงแบด&background=83ee03&color=fff'))

    # db.session.add(PrivateContact(firstname='ส้มโอ', lastname='โอเค',phone='081-111-1112', owner_id=1))
    
    db.session.commit()



if __name__ == "__main__":
    cli()
