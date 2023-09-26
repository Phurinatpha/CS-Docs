from io import BytesIO
from flask import (jsonify, render_template,request, url_for, flash, redirect, send_file)
import json
import base64
from sqlalchemy import desc
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.urls import url_parse
from sqlalchemy.sql import text, and_
# from flask_login import login_user, login_required, logout_user , current_user
import datetime
from app import app
from app import db
# from app import login_manager

from app.models.user import User
from app.models.Document import order_info, doc_info

# @login_manager.user_loader
# def load_user(user_id):
#     # since the user_id is just the primary key of our
#     # user table, use it in the query for the user
#     return AuthUser.query.get(int(user_id))



@app.route('/')
def home(): 
    #fix here
    return render_template("project/index_table.html")


@app.route('/base')
def base():
    return render_template("project/base.html")



@app.route('/form' , methods=('GET', 'POST'))
def form():
    if request.method == 'POST':
        doc_data = request.files.get('doc_data')
        #app.logger.debug("doc data :",doc_data)
        validated = True
        validated_dict = dict()
                # Read the contents of the uploaded file as bytes
        #ref_num = order_info.query.order_by(desc(order_info.id)).first().ref_num

        valid_keys = ['subject','ref_num', 'doc_date' ,'ref_year','user_id']

        # Access the uploaded file using request.files
        name_list =  request.form.get('name_list')
        name_list = name_list.split(",")
        name_list =  [i for i in name_list if i != ""]
        #app.logger.debug("name_list = ",name_list)
        # validate the input
        for key in request.form:
            if key not in valid_keys:
                continue
            value = request.form[key].strip()
            if not value or value == 'undefined':
                validated = False
                break
            app.logger.debug(value)
            validated_dict[key] = value

        if validated:
            order = order_info.query.filter(and_(order_info.ref_num == int(validated_dict['ref_num']) , \
                                             order_info.ref_year == int(validated_dict['ref_year']))).first()
            app.logger.debug("order :",order)
            if order == None:
                empty_order = order_info.query.filter(order_info.subject == None).first()
                #app.logger.debug("empty_order", empty_order)
                if empty_order != None:
                    app.logger.debug(empty_order)
                    db.session.delete(empty_order)
                    db.session.commit()
                order_entry = order_info(
                subject=validated_dict['subject'],
                doc_date=validated_dict['doc_date'],
                ref_num= validated_dict['ref_num'],
                ref_year=validated_dict['ref_year'],
                ref_name=name_list,
                user_id=validated_dict['user_id']
                )
                db.session.add(order_entry)
                db.session.commit()
                if doc_data != None :
                    doc_content = doc_data.read()
                    doc_entry = doc_info(
                    order_refnum = order_entry.ref_num,
                    order_refyear = order_entry.ref_year,
                    filename= str(validated_dict['ref_num'])+"/"+str(validated_dict['ref_year']),
                    doc_data=doc_content
                )
                    db.session.add(doc_entry)   
                
            else:
                app.logger.debug("update")

                order_entry = order.update(
                subject=validated_dict['subject'],
                doc_date=validated_dict['doc_date'],
                ref_name=name_list,
                user_id=validated_dict['user_id']
                )
                if doc_data != None :
                    doc_content = doc_data.read()
                    doc = doc_info.query.filter(and_(doc_info.order_refnum == order.ref_num,
                                             doc_info.order_refyear == order.ref_year)).first()
                    if doc != None: 
                        doc_entry = doc.update(
                        doc_data=doc_content
                        )
                    else:
                        doc_entry = doc_info(
                        order_refnum = order.ref_num,
                        order_refyear = order.ref_year,
                        filename= str(order.ref_num)+"/"+str(order.ref_year),
                        doc_data=doc_content)
                        db.session.add(doc_entry)
                

            db.session.commit()
            return home()

        return home()  
    return render_template("project/form.html")

@app.route('/preview_pdf', methods=('GET', 'POST'))
def preview_pdf():
    app.logger.debug("PDF PREVIEW")
    if request.method == 'POST':
        result = request.form.to_dict()
        app.logger.debug(result)
        num = result.get('ref_num', '')
        year = result.get('ref_year', '')
        app.logger.debug('ref_num',num,'ref_year',year)
        try:
            order = order_info.query.filter(and_(order_info.ref_num == int(num) , \
                                             order_info.ref_year == int(year))).first()
            doc = doc_info.query.filter(and_(doc_info.order_refnum == order.ref_num,
                                             doc_info.order_refyear == order.ref_year)).first()
            if doc is not None:  # Check if a document was found
                doc_data = doc.doc_data
                encoded_pdf_data = base64.b64encode(doc_data).decode('utf-8')
                doc_name = doc.filename
                return jsonify(doc_name = doc_name,doc_file = encoded_pdf_data)
            else:
                return "Document not found", 404  # Return a 404 error if document is not found
        except Exception as ex:
            app.logger.debug(ex)
            raise
    return ''



@app.route('/delete', methods=('GET', 'POST'))
def remove():
    app.logger.debug("REMOVE")
    if request.method == 'POST':
        result = request.form.to_dict()
        app.logger.debug(result)
        num = result.get('ref_num', '')
        year = result.get('ref_year', '')
        try:
            #contact = Contact.query.get(id_)
            order = order_info.query.filter(and_(order_info.ref_num == int(num) , \
                                             order_info.ref_year == int(year))).first()
            app.logger.debug("order :",order)
            latest_order = order_info.query.order_by(order_info.ref_num.desc(),order_info.ref_year.desc()).first()
            doc = doc_info.query.filter(and_(doc_info.order_refnum == order.ref_num,
                                             doc_info.order_refyear == order.ref_year)).first()
            app.logger.debug("latest :",latest_order)
            if doc != None:
                db.session.delete(doc)
            if order != latest_order:
                db.session.delete(order)
            else :
                order.mini_update(
                                    subject=None
                                  )
            db.session.commit()
        except Exception as ex:
            app.logger.debug(ex)
            raise
    return home()

@app.route('/search')
def search():
    return render_template("project/search.html")

@app.route('/access')
def access():
    return render_template("project/manage-access.html")

@app.route('/crash')
def crash():
    return 1/0

@app.route('/db')
def db_connection():
    try:
        with db.engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return '<h1>db works.</h1>'
    except Exception as e:
        return '<h1>db is broken.</h1>' + str(e)

@app.route("/user")
def user_data():
    documents = []
    db_documents = User.query.all()
    documents = list(map(lambda x: x.to_dict(), db_documents))
    app.logger.debug(str(len(documents)) + " already entry") 
    return jsonify(documents)

@app.route('/user_form' , methods=('GET', 'POST'))
def user_form():
    if request.method == 'POST':
        app.logger.debug("posted activate")
        validated = True
        validated_dict = dict()
        valid_keys = ['role','email']

        # Access the uploaded file using request.files
        id_ = request.form.get('id','')
        # validate the input
        for key in request.form:
            app.logger.debug(key)
            if key not in valid_keys:
                continue
            value = request.form[key].strip()
            if not value or value == 'undefined':
                validated = False
                break
            app.logger.debug(value)
            validated_dict[key] = value

        if validated:
            if not id_:
                app.logger.debug("add new user")
                # Create a new Document object with the uploaded file
                user_entry = User(
                firstname="",
                lastname="",
                role=bool(validated_dict['role']),
                email=validated_dict['email']
                )
                db.session.add(user_entry)
            else:
                user = User.query.get(id_)
                user_entry = user.update(
                email=validated_dict['email'],
                role=bool(validated_dict['role'])
                )
            #     if doc_data != None :
            #         doc_content = doc_data.read()
            #         doc = doc_info.query.filter(doc_info.order_id == id_).first()   
            #         doc_entry = doc.update(
            #         filename= str(validated_dict['ref_num'])+"/"+str(validated_dict['ref_year']),
            #         doc_data=doc_content
            #         )
            db.session.commit()
            return home()

        return home()  
    return ''

@app.route("/data")
def doc_data():
    documents = []
    db_documents = doc_info.query.all()
    documents = [doc.to_dict() for doc in db_documents]
    app.logger.debug(str(len(documents)) + " already entry")

    return jsonify(documents)

@app.route("/document")
def data():
    documents = []
    db_documents = order_info.query.order_by(order_info.ref_num.desc(), order_info.ref_year.desc())
    #db_documents = order_info.query.latest()
    #db_documents = db_documents.limit(10)
    documents = list(map(lambda x: x.to_dict(), db_documents))
    app.logger.debug(str(len(documents)) + " already entry")

    return jsonify(documents)
    #if request.method == 'POST':
       # documents = []
      #  db_documents = order_info.query.order_by(desc(order_info.id))
       # app.logger.debug("post doc")
       # result = request.form.to_dict()
       # page = result.get('page', '')
       # app.logger.debug("page :",page)
       # if page != 0 :
            # offset= int(page)*10
            # app.logger.debug(offset)
            # db_documents = db_documents.offset(offset).limit(10)
        # else:
            # db_documents = db_documents.offset(page).limit(10)
        # documents = list(map(lambda x: x.to_dict(), db_documents))
        # app.logger.debug("documents =", documents)
        # return jsonify(documents)

@app.route('/user_delete', methods=('GET', 'POST'))
def user_remove():
    if request.method == 'POST':
        result = request.form.to_dict()
        app.logger.debug(result)
        id_ = result.get('id', '')
        try:
            #contact = Contact.query.get(id_)
            order = User.query.get(id_)
            db.session.delete(order)
            db.session.commit()
        except Exception as ex:
            app.logger.debug(ex)
            raise
    return home()

@app.route('/download/<int:doc_id>')
def download(doc_id):
    doc =  doc_info.query.filter(doc_info.order_id == doc_id).first()
    app.logger.debug (doc)
    if doc:
        
        return send_file(
            BytesIO(doc.doc_data),
            mimetype='application/pdf',
            download_name=doc.filename+'.pdf',
            as_attachment=True
        )
    else:
        return "File not found"
# @app.route('/dashboard')
# def dashboard():
#     return 


