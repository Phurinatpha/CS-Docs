from flask.cli import FlaskGroup
from werkzeug.security import generate_password_hash
from app import app, db
from app.models.Document import order_info
from app.models.user import User
#from app.models.authuser import AuthUser, PrivateContact

cli = FlaskGroup(app)


@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command("seed_db")
def seed_db():  
    # db.session.add(User(firstname='สมชาย',lastname="ทรงแบด",role=True,email="flask@1234"))
    # db.session.add(User(firstname='น้องแคท',lastname="แซดบ๋อย",role=False,email="ksalf@4321"))
    db.session.add(User(firstname='แสงตะวัน',lastname="ภู่พุ่ม",role=True,email="saengtawan_p@cmu.ac.th"))
    db.session.add(User(firstname='ธีรภัทร์',lastname="นิลศิริ",role=True,email="thiraphat_n@cmu.ac.th"))
    db.session.add(User(firstname='',lastname="",role=True,email="panyawut_wayu@cmu.ac.th"))
    db.session.add(User(firstname='',lastname="",role=True,email="phurinat_phanuphong@cmu.ac.th"))
    db.session.commit()

    db.session.add(
        order_info(subject='แต่งตั้งเจ้าหน้าที่ปฏิบัติเกี่ยวกับการเรียนการสอนกระบวนวิชาระดับปริญญาตรี หลักสูตรนานาชาติ ประจำภาคการศึกษาที่ 1 ปีการศึกษา 2566', doc_date='2566-1-2',ref_num=1,ref_year='2566',ref_name=['ธีรภัทร์ นิลศิริ'],user_id='2'))
    db.session.add(
        order_info(subject='แต่งตั้งหัวหน้าสาขาวิชา ภาควิชาวิทยาการคอมพิวเตอร์ คณะวิทยาศาสตร์', doc_date='2566-1-4',ref_num=2,ref_year='2566',ref_name=['ธีรภัทร์ นิลศิริ'],user_id='2'))
    db.session.add(
        order_info(subject='แต่งตั้งคณะอนุกรรมการฝ่ายออกข้อสอบและตรวจข้อสอบ การสอบคัดเลือกนักเรียนเข้าค่ายโอลิมปิกวิชาการ คณะวิทยาศาสตร์ มหาวิทยาลัยเชียงใหม่ ประจำปีการศึกษา 2566', doc_date='2566-2-12',ref_num=3,ref_year='2566',ref_name=['แสงตะวัน ภู่พุ่ม'],user_id='1'))
    db.session.add(
        order_info(subject='แต่งตั้งคณะกรรมการประจำภาควิชาวิทยาการคอมพิวเตอร์ ในคณะวิทยาศาสตร์', doc_date='2566-3-8',ref_num=4,ref_year='2566',ref_name=['แสงตะวัน ภู่พุ่ม'],user_id='1'))
    db.session.add(
        order_info(subject='แต่งตั้งคณะอนุกรรมการดำเนินการสอบคัดเลือกบุคคลเข้าศึกษาในระดับบัณฑิตศึกษา หลักสูตรคอมพิวเตอร์ สาขาวิชาวิทยาการคอทพิวเตอร์ เทอม 1/2566 (รอบที่ 1)', doc_date='2566-3-26',ref_num=5,ref_year='2566',ref_name=['ธีรภัทร์ นิลศิริ'],user_id='2'))
    db.session.add(
        order_info(subject='แต่งตั้งอาจารย์ผู้ทำหน้าที่สอนและประสานงานการสอนกระบวนวิชาระดับปริญญาตรี หลักสูตรนานาชาติ ประจำภาคการศึกษาที่ 1 ปีการศึกษา 2566', doc_date='2566-4-15',ref_num=6,ref_year='2566',ref_name=['แสงตะวัน ภู่พุ่ม'],user_id='1'))
    db.session.add(
        order_info(subject='แต่งตั้งคณะกรรมการประเมินผลการทดลองปฏิบัติงานของพนักงานมหาวิทยาลัย ตำแหน่งธุรการ ตำแหน่งเลขที่ E180999 สังกัดภาควิชาวิทยาการคอมพิวเตอร์', doc_date='2566-4-29',ref_num=7,ref_year='2566',ref_name=['ธีรภัทร์ นิลศิริ'],user_id='2'))
    db.session.add(
        order_info(subject='แต่งตั้งคณะกรรมการสอบปริญญานิพนธ์  นายกอไก่ ออกไข่  630510204', doc_date='2566-5-10',ref_num=8,ref_year='2566',ref_name=['ธีรภัทร์ นิลศิริ'],user_id='2'))
    db.session.add(
        order_info(subject='แต่งตั้งคณะกรรมการคุมสอบกลางภาค ประจำภาคเรียนที่ 1 ปีการศึกษา 2566', doc_date='2566-5-30',ref_num=9,ref_year='2566',ref_name=['แสงตะวัน ภู่พุ่ม'],user_id='1'))
    db.session.add(
        order_info(subject='เปลี่ยนแปลงคณะกรรมการบริหารหลักสูตรระดับปริญญาตรี ประจำสาขาวิทยาการคอมพิวเตอร์', doc_date='2566-6-9',ref_num=10,ref_year='2566',ref_name=['แสงตะวัน ภู่พุ่ม'],user_id='1'))
    db.session.add(
        order_info(subject='แต่งตั้งเจ้าหน้าที่ปฏิบัติเกี่ยวกับการเรียนการสอนกระบวนวิชาระดับปริญญาโท หลักสูตรนานาชาติ ประจำภาคการศึกษาที่ 1 ปีการศึกษา 2566', doc_date='2566-6-15',ref_num=11,ref_year='2566',ref_name=['ธีรภัทร์ นิลศิริ'],user_id='2'))
    db.session.add(
        order_info(subject='แต่งตั้งหัวหน้าสาขาวิชา ภาควิชาวิทยาการคอมพิวเตอร์ คณะวิทยาศาสตร์', doc_date='2566-6-29',ref_num=12,ref_year='2566',ref_name=['ธีรภัทร์ นิลศิริ'],user_id='2'))
    db.session.add(
        order_info(subject='แต่งตั้งคณะอนุกรรมการฝ่ายออกข้อสอบและตรวจข้อสอบ การสอบคัดเลือกนักเรียนเข้าค่ายโอลิมปิกวิชาการ คณะวิทยาศาสตร์ มหาวิทยาลัยเชียงใหม่ ประจำปีการศึกษา 2566', doc_date='2566-7-1',ref_num=13,ref_year='2566',ref_name=['แสงตะวัน ภู่พุ่ม'],user_id='1'))
    db.session.add(
        order_info(subject='แต่งตั้งคณะกรรมการประจำภาควิชาวิทยาการคอมพิวเตอร์ ในคณะวิทยาศาสตร์', doc_date='2566-7-8',ref_num=14,ref_year='2566',ref_name=['แสงตะวัน ภู่พุ่ม'],user_id='1'))
    db.session.add(
        order_info(subject='แต่งตั้งคณะอนุกรรมการดำเนินการสอบคัดเลือกบุคคลเข้าศึกษาในระดับบัณฑิตศึกษา หลักสูตรคอมพิวเตอร์ สาขาวิชาวิทยาการคอทพิวเตอร์ เทอม 1/2566 (รอบที่ 2)', doc_date='2566-7-13',ref_num=15,ref_year='2566',ref_name=['ธีรภัทร์ นิลศิริ'],user_id='2'))
    db.session.add(
        order_info(subject='แต่งตั้งอาจารย์ผู้ทำหน้าที่สอนและประสานงานการสอนกระบวนวิชาระดับปริญญาตรี หลักสูตรนานาชาติ ประจำภาคการศึกษาที่ 1 ปีการศึกษา 2566', doc_date='2566-7-19',ref_num=16,ref_year='2566',ref_name=['แสงตะวัน ภู่พุ่ม'],user_id='1'))
    db.session.add(
        order_info(subject='แต่งตั้งคณะกรรมการประเมินผลการทดลองปฏิบัติงานของพนักงานมหาวิทยาลัย ตำแหน่งธุรการ ตำแหน่งเลขที่ E180999 สังกัดภาควิชาวิทยาการคอมพิวเตอร์', doc_date='2566-8-2',ref_num=17,ref_year='2566',ref_name=['ธีรภัทร์ นิลศิริ'],user_id='2'))
    db.session.add(
        order_info(subject='แต่งตั้งคณะกรรมการสอบปริญญานิพนธ์  นายเอก กระดาษ  630510204', doc_date='2566-8-15',ref_num=18,ref_year='2566',ref_name=['ธีรภัทร์ นิลศิริ'],user_id='2'))
    db.session.add(
        order_info(subject='แต่งตั้งคณะกรรมการคุมสอบกลางภาค ประจำภาคเรียนที่ 1 ปีการศึกษา 2566', doc_date='2566-9-5',ref_num=19,ref_year='2566',ref_name=['แสงตะวัน ภู่พุ่ม'],user_id='1'))
    db.session.add(
        order_info(subject='เปลี่ยนแปลงคณะกรรมการบริหารหลักสูตรระดับปริญญาตรี ประจำสาขาวิทยาการคอมพิวเตอร์', doc_date='2566-10-1',ref_num=20,ref_year='2566',ref_name=['แสงตะวัน ภู่พุ่ม'],user_id='1'))
    db.session.commit()



if __name__ == "__main__":
    cli()
