from io import BytesIO
from flask import (jsonify, render_template,request, url_for, flash, redirect, send_file)
import json
from sqlalchemy import desc
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.urls import url_parse
from sqlalchemy.sql import text
# from flask_login import login_user, login_required, logout_user , current_user

from app import app
from app import db
# from app import login_manager


from app.models.Document import order_info, doc_info

# @login_manager.user_loader
# def load_user(user_id):
#     # since the user_id is just the primary key of our
#     # user table, use it in the query for the user
#     return AuthUser.query.get(int(user_id))

@app.route('/')
def home(): 
    #fix here
    documents = order_info.query.order_by(desc(order_info.id))
    return render_template("project/index.html", documents=documents)

@app.route('/base')
def base():
    return render_template("project/base.html")

@app.route('/form' , methods=('GET', 'POST'))
def form():
    if request.method == 'POST':
        app.logger.debug("posted activate")
        validated = True
        validated_dict = dict()
        valid_keys = ['subject', 'doc_date', 'ref_num','ref_year','ref_name','user_id']

        # Access the uploaded file using request.files
        doc_data = request.files.get('doc_data')

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
            # Read the contents of the uploaded file as bytes

            doc_content = doc_data.read()
            app.logger.debug(doc_content)
            # Create a new Document object with the uploaded file
            order_entry = order_info(
                subject=validated_dict['subject'],
                doc_date=validated_dict['doc_date'],
                ref_num=validated_dict['ref_num'],
                ref_year=validated_dict['ref_year'],
                ref_name=validated_dict['ref_name'],
                user_id=validated_dict['user_id']
            )
            doc_entry = doc_info(
                filename= str(validated_dict['ref_num'])+"/"+str(validated_dict['ref_year']),
                doc_data=doc_content
            )
            db.session.add(order_entry)
            db.session.add(doc_entry)
            db.session.commit()
            return home()

        return home()  
    return render_template("project/form.html")

@app.route('/delete', methods=('GET', 'POST'))
def remove():
    app.logger.debug("REMOVE")
    if request.method == 'POST':
        result = request.form.to_dict()
        app.logger.debug(result)
        id_ = result.get('id', '')
        try:
            #contact = Contact.query.get(id_)
            order = order_info.query.get(id_)
            doc = doc_info.query.get(id_)
            db.session.delete(order)
            db.session.delete(doc)
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

@app.route("/document")
def data():
    documents = []
    db_documents = order_info.query.all()
    documents = list(map(lambda x: x.to_dict(), db_documents))
    app.logger.debug(str(len(documents)) + " already entry")
 
    return jsonify(documents)

@app.route('/download/<int:doc_id>')
def download(doc_id):
    doc = doc_info.query.get(doc_id)
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
