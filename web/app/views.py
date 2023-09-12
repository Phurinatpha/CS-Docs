from io import BytesIO
from flask import (jsonify, render_template,request, url_for, flash, redirect, send_file)
import json
import base64
from sqlalchemy import desc
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.urls import url_parse
from sqlalchemy.sql import text
from flask_login import login_user, login_required, logout_user , current_user

from app import app
from app import db
from app import login_manager

from app.models.authuser import AuthUser
from app.models.user import User
from app.models.Document import order_info, doc_info

# @login_manager.user_loader
# def load_user(user_id):
#     # since the user_id is just the primary key of our
#     # user table, use it in the query for the user
#     return AuthUser.query.get(int(user_id))

@app.route('/')
@login_required
def home(): 
    #fix here
    documents = []
    db_documents = order_info.query.all()
    documents = list(map(lambda x: x.to_dict(), db_documents))
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
        valid_keys = ['subject', 'doc_date', 'ref_num','ref_year','user_id']

        # Access the uploaded file using request.files
        doc_data = request.files.get('doc_data')
        name_list =  request.form.get('name_list')
        name_list = name_list.split(",")
        name_list =  [i for i in name_list if i != ""]
        app.logger.debug("name_list = ",name_list)
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
            # Create a new Document object with the uploaded file
            order_entry = order_info(
                subject=validated_dict['subject'],
                doc_date=validated_dict['doc_date'],
                ref_num=validated_dict['ref_num'],
                ref_year=validated_dict['ref_year'],
                ref_name=name_list,
                user_id=validated_dict['user_id']
            )
            db.session.add(order_entry)
            db.session.commit()
            doc_entry = doc_info(
                order_id = order_entry.id,
                filename= str(validated_dict['ref_num'])+"/"+str(validated_dict['ref_year']),
                doc_data=doc_content
            )
        
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
        id_ = result.get('id', '')
        try:
            doc = doc_info.query.filter(doc_info.order_id == id_).first()
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
        id_ = result.get('id', '')
        try:
            #contact = Contact.query.get(id_)
            order = order_info.query.get(id_)
            doc = doc_info.query.filter(doc_info.order_id == id_).first()
            if current_user.role == "admin":
                db.session.delete(order)
                db.session.commit()
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

@app.route("/user")
def user_data():
    documents = []
    db_documents = User.query.all()
    documents = list(map(lambda x: x.to_dict(), db_documents))
    app.logger.debug(str(len(documents)) + " already entry")
 
    return jsonify(documents)
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
    db_documents = order_info.query.all()
    documents = list(map(lambda x: x.to_dict(), db_documents))
    app.logger.debug(str(len(documents)) + " already entry")
 
    return jsonify(documents)

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

@app.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        # login code goes here
        email = request.form.get('email')
        password = request.form.get('password')
        remember = bool(request.form.get('remember'))


        user = AuthUser.query.filter_by(email=email).first()
 
        # check if the user actually exists
        # take the user-supplied password, hash it, and compare it to the
        # hashed password in the database
        if not user or not check_password_hash(user.password, password):
            flash('Please check your login details and try again.')
            # if the user doesn't exist or password is wrong, reload the page
            return redirect(url_for('login'))


        # if the above check passes, then we know the user has the right
        # credentials
        login_user(user, remember=remember)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('home')
        return redirect(next_page)
    return render_template('project/login.html')

@app.route('/signup', methods=('GET', 'POST'))
def signup():
    if request.method == 'POST':
        result = request.form.to_dict()
        app.logger.debug(str(result))
 
        validated = True
        validated_dict = {}
        valid_keys = ['email','firstname','lastname','role', 'password']


        # validate the input
        for key in result:
            app.logger.debug(str(key)+": " + str(result[key]))
            # screen of unrelated inputs
            if key not in valid_keys:
                continue


            value = result[key].strip()
            if not value or value == 'undefined':
                validated = False
                break
            validated_dict[key] = value
            # code to validate and add user to database goes here
        app.logger.debug("validation done")
        if validated:
            app.logger.debug('validated dict: ' + str(validated_dict))
            email = validated_dict['email']
            password = validated_dict['password']
            firstname = validated_dict['firstname']
            lastname = validated_dict['lastname']
            role = validated_dict['role']
            # if this returns a user, then the email already exists in database
            user = AuthUser.query.filter_by(email=email).first()


            if user:
                # if a user is found, we want to redirect back to signup
                # page so user can try again
                flash('Email address already exists')
                return redirect(url_for('signup'))


            # create a new user with the form data. Hash the password so
            # the plaintext version isn't saved.
            app.logger.debug("preparing to add")
            new_user = AuthUser(email=email,
                                password=generate_password_hash(
                                    password, method='sha256'))
            new_user_info = User(firstname=firstname,lastname=lastname,role=role,email=email)
            # add the new user to the database
            db.session.add(new_user)
            db.session.commit()
            db.session.add(new_user_info)
            db.session.commit()


        return redirect(url_for('login'))
    return render_template('project/signup.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our
    # user table, use it in the query for the user
    return AuthUser.query.get(int(user_id))