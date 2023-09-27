from io import BytesIO
from flask import jsonify, render_template,request, url_for, flash, redirect, send_file, session
import requests
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

import secrets
import string

# @login_manager.user_loader
# def load_user(user_id):
#     # since the user_id is just the primary key of our
#     # user table, use it in the query for the user
#     return AuthUser.query.get(int(user_id))

client_id = 'RHUnMd53w7Tb0NbSbBdj8D0rqchhtFpcA1gnNaMZ'  # The client ID assigned to you by the provider
client_secret = 'rt1cJmNSfKaqAbUmUC8J5XK0VQN9FZea0r4SPXSc'  # The client secret assigned to you by the provider

# here is the proble check in oauth config
redirect_uri = 'http://localhost:56789/oauth/callback'  # redirect_uri (This should match your OAuth configuration) 

oauth_scope = "cmuitaccount.basicinfo"
oauth_auth_url = "https://oauth.cmu.ac.th/v1/Authorize.aspx"
oauth_token_url = "https://oauth.cmu.ac.th/v1/GetToken.aspx"
wsapi_get_basicinfo_url = "https://misapi.cmu.ac.th/cmuitaccount/v1/api/cmuitaccount/basicinfo"



@app.route('/')
def home():
    if 'access_token' in session:
        # User is already authenticated, retrieve user data
        access_token = session['access_token']
        user_data = get_user_data(access_token)
        if user_data:
            
            return redirect(url_for("index"))
        else:
            auth_url = f"{oauth_auth_url}?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}&scope={oauth_scope}"
            return redirect(auth_url)
    else:
        # Redirect to the OAuth provider for authentication
        auth_url = f"{oauth_auth_url}?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}&scope={oauth_scope}"
        return redirect(auth_url)

@app.route('/oauth/callback')
def oauth_login():
    code = request.args.get('code')
    if code:
        # Exchange the authorization code for an access token
        access_token = get_oauth_token(code)
        if access_token:
            # Store the access token in the session
            session['access_token'] = access_token
            user_data = get_user_data(access_token)
            email = user_data.get('cmuitaccount')
            user = User.query.filter_by(email=email).first()
            app.logger.debug(user_data.get('firstname_TH') + ' and ' + user_data['lastname_TH'])
            app.logger.debug(user_data['cmuitaccount'])
            if user and user.firstname == '':
                app.logger.debug(user.email)
                app.logger.debug(user.firstname)
                user_entry = user.update_name(
                    firstname=user_data.get('firstname_TH'),
                    lastname=user_data['lastname_TH']
                )
                db.session.commit()
                login_user(user)
            return redirect(url_for('index'))
        else:
            return 'Error getting access token'
    else:
        # error = request.args.get('error')
        # error_description = request.args.get('error_description')
        # return f'Error: {error}, Description: {error_description}'
        return redirect(url_for('home'))

@app.route('/logout')
@login_required
def logout():
    app.logger.debug("session : " + session)
    session.clear()
    logout_user()
    return redirect(url_for('home'))

def get_oauth_token(code):
    payload = {
        'code': code,
        'client_id': client_id,
        'client_secret': client_secret,
        'redirect_uri': redirect_uri,
        'grant_type': 'authorization_code'
    }
    response = requests.post(oauth_token_url, data=payload)
    if response.status_code == 200:
        data = response.json()
        return data.get('access_token')
    else:
        return None

def get_user_data(access_token):
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Cache-Control': 'no-cache'
    }
    response = requests.get(wsapi_get_basicinfo_url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return None

@app.route('/index')
def index(): 
    #fix here
    if 'access_token' in session:
        # User is already authenticated, retrieve user data
        access_token = session['access_token']
        user_data = get_user_data(access_token)
        if user_data:
            
            user_data_ = {
                'name': user_data.get('firstname_TH') + " " + user_data.get('lastname_TH'),
                'email': user_data.get('cmuitaccount')
                }
            return render_template("project/index_table.html",user=user_data_)
        else:
            auth_url = f"{oauth_auth_url}?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}&scope={oauth_scope}"
            return redirect(auth_url)
    else:
        # Redirect to the OAuth provider for authentication
        auth_url = f"{oauth_auth_url}?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}&scope={oauth_scope}"
        return redirect(auth_url)

@app.route('/base')
def base():
    if 'access_token' in session:
        # User is already authenticated, retrieve user data
        access_token = session['access_token']
        user_data = get_user_data(access_token)
        if user_data:
            user_data_ = {
                'name': user_data.get('firstname_TH') + " " + user_data.get('lastname_TH'),
                'email': user_data.get('cmuitaccount')
                }
            return render_template("project/base.html",user=user_data_)
        else:
            auth_url = f"{oauth_auth_url}?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}&scope={oauth_scope}"
            return redirect(auth_url)
    else:
        # Redirect to the OAuth provider for authentication
        auth_url = f"{oauth_auth_url}?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}&scope={oauth_scope}"
        return redirect(auth_url)

@app.route('/form' , methods=('GET', 'POST'))
def form():
    if request.method == 'POST':
        doc_data = request.files.get('doc_data')
        #app.logger.debug("doc data :",doc_data)
        validated = True
        validated_dict = dict()
                # Read the contents of the uploaded file as bytes
        ref_num = order_info.query.order_by(desc(order_info.id)).first().ref_num

        valid_keys = ['subject','ref_num', 'doc_date' ,'ref_year','user_id']

        # Access the uploaded file using request.files
        name_list =  request.form.get('name_list')
        id_ = request.form.get('id','')
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
            if not id_:
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
                    order_id = order_entry.id,
                    filename= str(ref_num)+"/"+str(validated_dict['ref_year']),
                    doc_data=doc_content
                )
                    db.session.add(doc_entry)   
            else:
                app.logger.debug("update")
                order = order_info.query.get(id_)
                order_entry = order.update(
                subject=validated_dict['subject'],
                ref_num=validated_dict['ref_num'],
                doc_date=validated_dict['doc_date'],
                ref_year=validated_dict['ref_year'],
                ref_name=name_list,
                user_id=validated_dict['user_id']
                )
                if doc_data != None :
                    doc_content = doc_data.read()
                    doc = doc_info.query.filter(doc_info.order_id == id_).first()
                    if doc != None: 
                        doc_entry = doc.update(
                        doc_data=doc_content
                        )
                    else:
                        doc_entry = doc_info(
                        order_id = order.id,
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
            app.logger.debug("order :",order)
            latest_order = order_info.query.order_by(desc(order_info.id)).first()
            doc = doc_info.query.filter(doc_info.order_id == id_).first()
            app.logger.debug("latest :",latest_order)
            if doc != None:
                db.session.delete(doc)
            if order != latest_order:
                db.session.delete(order)
            else :
                order_entry = order.mini_update(
                subject=None
                )
            db.session.commit()
        except Exception as ex:
            app.logger.debug(ex)
            raise
    return home()()

@app.route('/search')
def search():
    if 'access_token' in session:
        # User is already authenticated, retrieve user data
        access_token = session['access_token']
        user_data = get_user_data(access_token)
        if user_data:
            user_data_ = {
                'name': user_data.get('firstname_TH') + " " + user_data.get('lastname_TH'),
                'email': user_data.get('cmuitaccount')
                }
            
            return render_template("project/search.html",user=user_data_)
        else:
            auth_url = f"{oauth_auth_url}?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}&scope={oauth_scope}"
            return redirect(auth_url)
    else:
        # Redirect to the OAuth provider for authentication
        auth_url = f"{oauth_auth_url}?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}&scope={oauth_scope}"
        return redirect(auth_url)


@app.route('/access')
def access():
    if 'access_token' in session:
        # User is already authenticated, retrieve user data
        access_token = session['access_token']
        user_data = get_user_data(access_token)
        if user_data:
            user_data_ = {
                'name': user_data.get('firstname_TH') + " " + user_data.get('lastname_TH'),
                'email': user_data.get('cmuitaccount')
                }
            return render_template("project/manage-access.html",user=user_data_)
        else:
            auth_url = f"{oauth_auth_url}?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}&scope={oauth_scope}"
            return redirect(auth_url)
    else:
        # Redirect to the OAuth provider for authentication
        auth_url = f"{oauth_auth_url}?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}&scope={oauth_scope}"
        return redirect(auth_url)
    

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
    db_documents = order_info.query.order_by(desc(order_info.id))
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

# @app.route('/login', methods=('GET', 'POST'))
# def login():
#     if request.method == 'POST':
#         # login code goes here
#         email = request.form.get('email')
#         password = request.form.get('password')
#         remember = bool(request.form.get('remember'))


#         user = User.query.filter_by(email=email).first()
 
#         # check if the user actually exists
#         # take the user-supplied password, hash it, and compare it to the
#         # hashed password in the database
#         if not user or not check_password_hash(user.password, password):
#             flash('Please check your login details and try again.')
#             # if the user doesn't exist or password is wrong, reload the page
#             return redirect(url_for('login'))
#         # if the above check passes, then we know the user has the right
#         # credentials
#         login_user(user, remember=remember)
#         next_page = request.args.get('next')
#         if not next_page or url_parse(next_page).netloc != '':
#             next_page = url_for('home')
#         return redirect(next_page)
#     return render_template('project/login.html')



@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our
    # user table, use it in the query for the user
    return User.query.get(int(user_id))