from io import BytesIO
from flask import jsonify, render_template,request, url_for, flash, redirect, send_file, session
import requests
import json
import base64
from sqlalchemy import desc
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.urls import url_parse
from sqlalchemy.sql import text, and_
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import datetime
from app import app
from app import db
from app import login_manager

from app.models.user import User
from app.models.Document import order_info, doc_info


client_id = 'RHUnMd53w7Tb0NbSbBdj8D0rqchhtFpcA1gnNaMZ'  # The client ID assigned to you by the provider
client_secret = 'rt1cJmNSfKaqAbUmUC8J5XK0VQN9FZea0r4SPXSc'  # The client secret assigned to you by the provider

# here is the proble check in oauth config
redirect_uri = 'http://localhost:56789/oauth/callback'  # redirect_uri (This should match your OAuth configuration) 

oauth_scope = "cmuitaccount.basicinfo"
oauth_auth_url = "https://oauth.cmu.ac.th/v1/Authorize.aspx"
oauth_token_url = "https://oauth.cmu.ac.th/v1/GetToken.aspx"
wsapi_get_basicinfo_url = "https://misapi.cmu.ac.th/cmuitaccount/v1/api/cmuitaccount/basicinfo"

login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our
    # user table, use it in the query for the user
    return User.query.get(int(user_id))

def generate_auth_url():
    return f"{oauth_auth_url}?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}&scope={oauth_scope}"

@app.route('/')
def home():
    if 'access_token' in session:
        app.logger.debug("homeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee")

        return redirect(url_for("index"))
    else:
        return redirect(generate_auth_url())

@app.route('/oauth/callback')
def oauth_login():
    code = request.args.get('code')
    if code:
        app.logger.debug("-----------------------------in if code callback-----------------------------")

        access_token = get_oauth_token(code)
        if access_token:
            app.logger.debug("-----------------------------in if access callback-----------------------------")
            session['access_token'] = access_token
            user_data = get_user_data(access_token)
            email = user_data.get('cmuitaccount')
            user = User.query.filter_by(email=email).first()
            
            if user:
                if user.firstname == '':
                    app.logger.debug("-----------------------------in if user callback-----------------------------")
                    new_firstname = user_data.get('firstname_TH')
                    new_lastname = user_data['lastname_TH']
                    user.update_name(new_firstname, new_lastname)
                    db.session.commit()
                    return redirect(url_for('index'))   
                else:
                    return redirect(url_for('index'))   
            else:
                app.logger.debug("-----------------------------in else user callback-----------------------------")
                session.clear() #DO NOT MOVE OR DELETE, prevent who can not access
                return 'Access denie' #Can edit here for good look view
        else:
            return 'Error getting access token'
    # error = request.args.get('error')
    # error_description = request.args.get('error_description')
    return redirect(url_for('home'))

@app.route('/logout')
def logout():
    session.clear()
    # logout_user()
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
    if 'access_token' in session:
        access_token = session['access_token']
        user_data = get_user_data(access_token)
        email = user_data.get('cmuitaccount')
        user = User.query.filter_by(email=email).first()
        if user:
            usr_email = user.email
            firstname = user.firstname
            lastname = user.lastname
            user_data_ = {
                'id' : user.id,
                'name': firstname + " " + lastname,
                'email': usr_email
            }
        return render_template("project/index_table.html", user=user_data_)
    
    return redirect(generate_auth_url())


    # return render_template("project/index_table.html") #for without login test

# @app.route('/base')
# def base():
#     if 'access_token' in session:
#         access_token = session['access_token']
#         user_data = get_user_data(access_token)
#         if user_data:
#             user_data_ = {
#                 'name': user_data.get('firstname_TH') + " " + user_data.get('lastname_TH'),
#                 'email': user_data.get('cmuitaccount')
#             }
#             return render_template("project/index_table.html", user=user_data_)
    
#     return redirect(generate_auth_url())
8



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
    return render_template("project/index_table.html")

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
            order = order_info.query.filter(and_(order_info.ref_num == int(num) ,
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
        access_token = session['access_token']
        user_data = get_user_data(access_token)
        if user_data:
            user_data_ = {
                'name': user_data.get('firstname_TH') + " " + user_data.get('lastname_TH'),
                'email': user_data.get('cmuitaccount')
            }
            return render_template("project/manage-access.html", user=user_data_)
    
    return redirect(generate_auth_url())
    

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
    db_documents = User.query.order_by(User.id.desc())
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
                app.logger.debug("role1 : " + validated_dict['role'])
                # Create a new Document object with the uploaded file
                if validated_dict['role'] == "True":
                    role_ = True
                elif validated_dict['role'] == "False":
                    role_ = False
                app.logger.debug("role2 : " + str(role_))
                user_entry = User(
                firstname="",
                lastname="",
                role=role_,
                email=validated_dict['email']
                )
                db.session.add(user_entry)
            else:
                user = User.query.get(id_)
                app.logger.debug("role : " + validated_dict['role'])
                if validated_dict['role'] == "True":
                    role_ = True
                elif validated_dict['role'] == "False":
                    role_ = False
                app.logger.debug("role2 : " + str(role_))
                user_entry = user.update(
                email=validated_dict['email'],
                role=role_
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
    limit = int(request.args.get('limit', 1000))
    documents = []
    db_documents = order_info.query.order_by(order_info.ref_year.desc(), order_info.ref_num.desc())
    #db_documents = order_info.query.latest()
    #db_documents = db_documents.limit(10)
    documents = list(map(lambda x: x.to_dict(), db_documents))
    documents.insert(0, len(documents))
    documents = documents[:limit]
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
