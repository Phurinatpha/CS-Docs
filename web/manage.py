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
    # db.session.add(User(firstname='สมชาย',lastname="ทรงแบด",is_admin=True,email="flask@1234"))
    # db.session.add(User(firstname='น้องแคท',lastname="แซดบ๋อย",is_admin=False,email="ksalf@4321"))
    db.session.add(User(firstname='แสงตะวัน',lastname="ภู่พุ่ม",is_admin=True,email="saengtawan_p@cmu.ac.th"))
    db.session.add(User(firstname='ธีรภัทร์',lastname="นิลศิริ",is_admin=True,email="thiraphat_n@cmu.ac.th"))
    db.session.add(User(firstname='',lastname="",is_admin=True,email="panyawut_wayu@cmu.ac.th"))
    db.session.add(User(firstname='',lastname="",is_admin=True,email="phurinat_phanuphong@cmu.ac.th"))
    db.session.commit()

    db.session.add(
        order_info(subject='แต่งตั้งเจ้าหน้าที่ปฏิบัติเกี่ยวกับการเรียนการสอนกระบวนวิชาระดับปริญญาตรี หลักสูตรนานาชาติ ประจำภาคการศึกษาที่ 1 ปีการศึกษา 2566', order_date='2566-1-2',order_num=1,order_year='2566',ref_name=['ธีรภัทร์ นิลศิริ'],user_id='2'))
    db.session.add(
        order_info(subject='แต่งตั้งหัวหน้าสาขาวิชา ภาควิชาวิทยาการคอมพิวเตอร์ คณะวิทยาศาสตร์', order_date='2566-1-4',order_num=2,order_year='2566',ref_name=['ธีรภัทร์ นิลศิริ'],user_id='2'))
    db.session.add(
        order_info(subject='แต่งตั้งคณะอนุกรรมการฝ่ายออกข้อสอบและตรวจข้อสอบ การสอบคัดเลือกนักเรียนเข้าค่ายโอลิมปิกวิชาการ คณะวิทยาศาสตร์ มหาวิทยาลัยเชียงใหม่ ประจำปีการศึกษา 2566', order_date='2566-2-12',order_num=3,order_year='2566',ref_name=['แสงตะวัน ภู่พุ่ม'],user_id='1'))
    db.session.add(
        order_info(subject='แต่งตั้งคณะกรรมการประจำภาควิชาวิทยาการคอมพิวเตอร์ ในคณะวิทยาศาสตร์', order_date='2566-3-8',order_num=4,order_year='2566',ref_name=['แสงตะวัน ภู่พุ่ม'],user_id='1'))
    db.session.add(
        order_info(subject='แต่งตั้งคณะอนุกรรมการดำเนินการสอบคัดเลือกบุคคลเข้าศึกษาในระดับบัณฑิตศึกษา หลักสูตรคอมพิวเตอร์ สาขาวิชาวิทยาการคอทพิวเตอร์ เทอม 1/2566 (รอบที่ 1)', order_date='2566-3-26',order_num=5,order_year='2566',ref_name=['ธีรภัทร์ นิลศิริ'],user_id='2'))
    db.session.add(
        order_info(subject='แต่งตั้งอาจารย์ผู้ทำหน้าที่สอนและประสานงานการสอนกระบวนวิชาระดับปริญญาตรี หลักสูตรนานาชาติ ประจำภาคการศึกษาที่ 1 ปีการศึกษา 2566', order_date='2566-4-15',order_num=6,order_year='2566',ref_name=['แสงตะวัน ภู่พุ่ม'],user_id='1'))
    db.session.add(
        order_info(subject='แต่งตั้งคณะกรรมการประเมินผลการทดลองปฏิบัติงานของพนักงานมหาวิทยาลัย ตำแหน่งธุรการ ตำแหน่งเลขที่ E180999 สังกัดภาควิชาวิทยาการคอมพิวเตอร์', order_date='2566-4-29',order_num=7,order_year='2566',ref_name=['ธีรภัทร์ นิลศิริ'],user_id='2'))
    db.session.add(
        order_info(subject='แต่งตั้งคณะกรรมการสอบปริญญานิพนธ์  นายกอไก่ ออกไข่  630510204', order_date='2566-5-10',order_num=8,order_year='2566',ref_name=['ธีรภัทร์ นิลศิริ'],user_id='2'))
    db.session.add(
        order_info(subject='แต่งตั้งคณะกรรมการคุมสอบกลางภาค ประจำภาคเรียนที่ 1 ปีการศึกษา 2566', order_date='2566-5-30',order_num=9,order_year='2566',ref_name=['แสงตะวัน ภู่พุ่ม'],user_id='1'))
    db.session.add(
        order_info(subject='เปลี่ยนแปลงคณะกรรมการบริหารหลักสูตรระดับปริญญาตรี ประจำสาขาวิทยาการคอมพิวเตอร์', order_date='2566-6-9',order_num=10,order_year='2566',ref_name=['แสงตะวัน ภู่พุ่ม'],user_id='1'))
    db.session.add(
        order_info(subject='แต่งตั้งเจ้าหน้าที่ปฏิบัติเกี่ยวกับการเรียนการสอนกระบวนวิชาระดับปริญญาโท หลักสูตรนานาชาติ ประจำภาคการศึกษาที่ 1 ปีการศึกษา 2566', order_date='2566-6-15',order_num=11,order_year='2566',ref_name=['ธีรภัทร์ นิลศิริ'],user_id='2'))
    db.session.add(
        order_info(subject='แต่งตั้งหัวหน้าสาขาวิชา ภาควิชาวิทยาการคอมพิวเตอร์ คณะวิทยาศาสตร์', order_date='2566-6-29',order_num=12,order_year='2566',ref_name=['ธีรภัทร์ นิลศิริ'],user_id='2'))
    db.session.add(
        order_info(subject='แต่งตั้งคณะอนุกรรมการฝ่ายออกข้อสอบและตรวจข้อสอบ การสอบคัดเลือกนักเรียนเข้าค่ายโอลิมปิกวิชาการ คณะวิทยาศาสตร์ มหาวิทยาลัยเชียงใหม่ ประจำปีการศึกษา 2566', order_date='2566-7-1',order_num=13,order_year='2566',ref_name=['แสงตะวัน ภู่พุ่ม'],user_id='1'))
    db.session.add(
        order_info(subject='แต่งตั้งคณะกรรมการประจำภาควิชาวิทยาการคอมพิวเตอร์ ในคณะวิทยาศาสตร์', order_date='2566-7-8',order_num=14,order_year='2566',ref_name=['แสงตะวัน ภู่พุ่ม'],user_id='1'))
    db.session.add(
        order_info(subject='แต่งตั้งคณะอนุกรรมการดำเนินการสอบคัดเลือกบุคคลเข้าศึกษาในระดับบัณฑิตศึกษา หลักสูตรคอมพิวเตอร์ สาขาวิชาวิทยาการคอทพิวเตอร์ เทอม 1/2566 (รอบที่ 2)', order_date='2566-7-13',order_num=15,order_year='2566',ref_name=['ธีรภัทร์ นิลศิริ'],user_id='2'))
    db.session.add(
        order_info(subject='แต่งตั้งอาจารย์ผู้ทำหน้าที่สอนและประสานงานการสอนกระบวนวิชาระดับปริญญาตรี หลักสูตรนานาชาติ ประจำภาคการศึกษาที่ 1 ปีการศึกษา 2566', order_date='2566-7-19',order_num=16,order_year='2566',ref_name=['แสงตะวัน ภู่พุ่ม'],user_id='1'))
    db.session.add(
        order_info(subject='แต่งตั้งคณะกรรมการประเมินผลการทดลองปฏิบัติงานของพนักงานมหาวิทยาลัย ตำแหน่งธุรการ ตำแหน่งเลขที่ E180999 สังกัดภาควิชาวิทยาการคอมพิวเตอร์', order_date='2566-8-2',order_num=17,order_year='2566',ref_name=['ธีรภัทร์ นิลศิริ'],user_id='2'))
    db.session.add(
        order_info(subject='แต่งตั้งคณะกรรมการสอบปริญญานิพนธ์  นายเอก กระดาษ  630510204', order_date='2566-8-15',order_num=18,order_year='2566',ref_name=['ธีรภัทร์ นิลศิริ'],user_id='2'))
    db.session.add(
        order_info(subject='แต่งตั้งคณะกรรมการคุมสอบกลางภาค ประจำภาคเรียนที่ 1 ปีการศึกษา 2566', order_date='2566-9-5',order_num=19,order_year='2566',ref_name=['แสงตะวัน ภู่พุ่ม'],user_id='1'))
    db.session.add(
        order_info(subject='เปลี่ยนแปลงคณะกรรมการบริหารหลักสูตรระดับปริญญาตรี ประจำสาขาวิทยาการคอมพิวเตอร์', order_date='2566-10-1',order_num=20,order_year='2566',ref_name=['แสงตะวัน ภู่พุ่ม'],user_id='1'))
    db.session.commit()



if __name__ == "__main__":
    cli()
