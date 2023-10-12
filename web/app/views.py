from io import BytesIO
from flask import jsonify, render_template,request, url_for, flash, redirect, send_file, session
import requests
import json
import base64
from sqlalchemy.sql import text, and_
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from app import app
from app import db
from app import login_manager

from app.models.user import User
from app.models.Document import order_info, doc_info


client_id=app.config['CLIENT_ID']
client_secret=app.config['CLIENT_SECERT']
redirect_uri = app.config['REDIRECT_URI']
oauth_scope = app.config['SCOPE']
oauth_auth_url = app.config['AUTH_URL']
oauth_token_url = app.config['TOKEN_URL']
wsapi_get_basicinfo_url = app.config['GET_USER']

login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def generate_auth_url():

    return f"{oauth_auth_url}?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}&scope={oauth_scope}"

@app.route('/')
def home():
    if 'access_token' in session:
        return redirect(url_for("index"))
    else:
        return redirect(generate_auth_url())

@app.route('/403')
def forbidden():
    return render_template("project/403.html")

@app.route('/oauth/callback')
def oauth_login():
    code = request.args.get('code')
    if code:
        access_token = get_oauth_token(code)
        if access_token:
            session['access_token'] = access_token
            user_data = get_user_data(access_token)
            email = user_data.get('cmuitaccount')
            user = User.query.filter_by(email=email).first()
            
            if user:
                if user.firstname == '':
                    new_firstname = user_data.get('firstname_TH')
                    new_lastname = user_data['lastname_TH']
                    user.update_name(new_firstname, new_lastname)
                    db.session.commit()
                    return redirect(url_for('index'))   
                else:
                    return redirect(url_for('index'))   
            else:
                session.clear() #DO NOT MOVE OR DELETE, prevent who can not access
                return render_template("project/403.html")
        else:
            return redirect(url_for('index')) 

    return redirect(url_for('home'))

@app.route('/logout')
def logout():
    session.clear()
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
                'is_admin' : user.is_admin,
                'name': firstname + " " + lastname,
                'email': usr_email
            }
        return render_template("project/index_table.html", user=user_data_)
    
    return redirect(generate_auth_url())

@app.route('/form' , methods=('GET', 'POST'))
def form():
    access_token = session['access_token']
    user_data = get_user_data(access_token)
    email = user_data.get('cmuitaccount')
    user = User.query.filter_by(email=email).first()
    if user.is_admin == True:
        if request.method == 'POST':
            doc_data = request.files.get('doc_data')
            #app.logger.debug("doc data :",doc_data)
            validated = True
            validated_dict = dict()
            delete_pdf = request.form.get('delete_pdf', '')
            app.logger.debug("delete_pdf ",delete_pdf)
            valid_keys = ['subject','order_num', 'order_date' ,'order_year','user_id']

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
            order = order_info.query.filter(and_(order_info.order_num == int(validated_dict['order_num']) , \
                                             order_info.order_year == int(validated_dict['order_year']))).first()
            app.logger.debug("order :",order)
            if order == None:
                empty_order = order_info.query.filter(and_(order_info.subject == None,
                                                           order_info.order_year == int(validated_dict['order_year']))).first()
                #app.logger.debug("empty_order", empty_order)
                if empty_order != None:
                    app.logger.debug(empty_order)
                    db.session.delete(empty_order)
                    db.session.commit()
                order_entry = order_info(
                subject=validated_dict['subject'],
                order_date=validated_dict['order_date'],
                order_num= validated_dict['order_num'],
                order_year=validated_dict['order_year'],
                ref_name=name_list,
                user_id=validated_dict['user_id']
                )
                db.session.add(order_entry)
                db.session.commit()
                if doc_data != None :
                    doc_content = doc_data.read()
                    doc_entry = doc_info(
                    order_refnum = order_entry.order_num,
                    order_refyear = order_entry.order_year,
                    filename= str(validated_dict['order_num'])+"/"+str(validated_dict['order_year']),
                    doc_data=doc_content
                    )
                    db.session.add(doc_entry)
            else:
                app.logger.debug("update")
                edit_doc = order_info.query.filter(and_(order_info.order_num == validated_dict['order_num'],
                                             order_info.order_year == validated_dict['order_year'])).first()
                order_entry = order.update(
                subject=validated_dict['subject'],
                order_date=validated_dict['order_date'],
                ref_name=name_list,
                user_id=edit_doc.user_id
                )
                if doc_data != None :
                    doc = doc_info.query.filter(and_(doc_info.order_refnum == order.order_num,
                                             doc_info.order_refyear == order.order_year)).first()
                    doc_content = doc_data.read()
                    if doc != None: 
                        doc_entry = doc.update(
                        doc_data=doc_content
                            )
                    else :
                        doc_entry = doc_info(
                        order_refnum = order.order_num,
                        order_refyear = order.order_year,
                        filename= str(order.order_num)+"/"+str(order.order_year),
                        doc_data=doc_content)
                        db.session.add(doc_entry)
                else:
                    doc = doc_info.query.filter(and_(doc_info.order_refnum == order.order_num,
                                             doc_info.order_refyear == order.order_year)).first()
                    if doc != None:
                        if  delete_pdf == 'true':
                            db.session.delete(doc)
                

            db.session.commit()
                
            return home()
    else:
        flash("You do not have permission.")
        return home()
    return render_template("project/index_table.html")

@app.route('/preview_pdf', methods=('GET', 'POST'))
def preview_pdf():
    app.logger.debug("PDF PREVIEW")
    if request.method == 'POST':
        result = request.form.to_dict()
        app.logger.debug(result)
        num = result.get('order_num', '')
        year = result.get('order_year', '')
        app.logger.debug('order_num',num,'order_year',year)
        try:
            order = order_info.query.filter(and_(order_info.order_num == int(num) , \
                                             order_info.order_year == int(year))).first()
            doc = doc_info.query.filter(and_(doc_info.order_refnum == order.order_num,
                                             doc_info.order_refyear == order.order_year)).first()
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
        num = result.get('order_num', '')
        year = result.get('order_year', '')
        access_token = session['access_token']
        user_data = get_user_data(access_token)
        email = user_data.get('cmuitaccount')
        user = User.query.filter_by(email=email).first()
        if user.is_admin == True:
            try:
                #contact = Contact.query.get(id_)
                order = order_info.query.filter(and_(order_info.order_num == int(num) ,
                                                order_info.order_year == int(year))).first()
                app.logger.debug("order :",order)
                latest_order = order_info.query.filter(and_(order_info.order_num == int(num) ,
                                                order_info.order_year == int(year))).order_by(order_info.order_year.desc(),order_info.order_num.desc()).first()
                doc = doc_info.query.filter(and_(doc_info.order_refnum == order.order_num,
                                                doc_info.order_refyear == order.order_year)).first()
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
        else:
            flash("You do not have permission to delete.")
    return home()

@app.route('/search')
def search():
    if 'access_token' in session:
        # User is already authenticated, retrieve user data
        access_token = session['access_token']
        user_data = get_user_data(access_token)
        email = user_data.get('cmuitaccount')
        user = User.query.filter_by(email=email).first()
        if user_data:
            user_data_ = {
                'id' : user.id,
                'is_admin' : user.is_admin,
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
        email = user_data.get('cmuitaccount')
        user = User.query.filter_by(email=email).first()
        if user.is_admin != True:
            return redirect(url_for('home'))
        if user_data:
            app.logger.debug(user.id)
            user_data_ = {
                'id' : user.id,
                'is_admin' : user.is_admin,
                'name': user_data.get('firstname_TH') + " " + user_data.get('lastname_TH'),
                'email': user_data.get('cmuitaccount')
            }
            user_email = user.email
            return render_template("project/manage-access.html", user=user_data_,user_email=user_email)
    
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

@app.route('/user_form' , methods=('GET', 'POST'))
def user_form():
    access_token = session['access_token']
    user_data = get_user_data(access_token)
    email = user_data.get('cmuitaccount')
    user = User.query.filter_by(email=email).first()
    if user.is_admin == True:
        if request.method == 'POST':
            app.logger.debug("posted activate")
            validated = True
            validated_dict = dict()
            valid_keys = ['is_admin','email']

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
                    app.logger.debug("is_admin1 : " + validated_dict['is_admin'])
                    # Create a new Document object with the uploaded file
                    if validated_dict['is_admin'] == "True":
                        is_admin_ = True
                    elif validated_dict['is_admin'] == "False":
                        is_admin_ = False
                    app.logger.debug("is_admin2 : " + str(is_admin_))
                    user_entry = User(
                    firstname="",
                    lastname="",
                    is_admin=is_admin_,
                    email=validated_dict['email']
                    )
                    db.session.add(user_entry)
                else:
                    user = User.query.get(id_)
                    app.logger.debug("is_admin : " + validated_dict['is_admin'])
                    if validated_dict['is_admin'] == "True":
                        is_admin_ = True
                    elif validated_dict['is_admin'] == "False":
                        is_admin_ = False
                    app.logger.debug("is_admin2 : " + str(is_admin_))
                    user_entry = user.update_is_admin(
                    is_admin=is_admin_
                    )
                #     if doc_data != None :
                #         doc_content = doc_data.read()
                #         doc = doc_info.query.filter(doc_info.order_id == id_).first()   
                #         doc_entry = doc.update(
                #         filename= str(validated_dict['order_num'])+"/"+str(validated_dict['order_year']),
                #         doc_data=doc_content
                #         )
                db.session.commit()
                return home()

            return home()
        else:
            flash("You do not have permission to delete.")
            return home()
    return ''

@app.route("/data")
def doc_data():
    documents = []
    db_documents = doc_info.query.all()
    documents = [doc.to_dict() for doc in db_documents]
    app.logger.debug(str(len(documents)) + " already entry")

    return jsonify(documents)

@app.route("/user")
def user_data():
    documents = []
    limit = int(request.args.get('limit', 100000000))
    db_documents = User.query.filter(User.email != None).order_by(User.id.desc())
    #is_null = User.query.filter(User.email == None ).count()
    documents = list(map(lambda x: x.to_dict(), db_documents))
    documents.insert(0, len(documents) )
    documents = documents[:limit]
    app.logger.debug(str(len(documents)) + " already entry") 
    return jsonify(documents)

@app.route("/document" , methods=('GET', 'POST'))
def data():
    documents = []
    if request.method == 'POST':
        year = request.form.get('order_year', '')
        find_refnum = order_info.query.filter(order_info.order_year == int(year) ).order_by(order_info.order_num.desc()).first()
        app.logger.debug("find_refnum",find_refnum)
        if find_refnum != None: 
            return jsonify(find_refnum.to_dict())
        else:
            return {'order_num' : "0/0"}
    limit = int(request.args.get('limit', 100000000))
    
    db_documents = order_info.query.order_by(order_info.order_year.desc(), order_info.order_num.desc())
    is_null = order_info.query.filter(order_info.subject == None ).count()
    app.logger.debug("is_null",is_null)
    #db_documents = order_info.query.latest()
    #db_documents = db_documents.limit(10)
    documents = list(map(lambda x: x.to_dict(), db_documents))
    documents.insert(0, len(documents) - is_null)
    documents = documents[:limit]
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

@app.route('/user_delete', methods=('GET', 'POST'))
def user_remove():
    if request.method == 'POST':
        result = request.form.to_dict()
        app.logger.debug(result)
        id_ = result.get('id', '')
        is_null = order_info.query.filter(order_info.user_id == id_ ).first()
        access_token = session['access_token']
        user_data = get_user_data(access_token)
        email = user_data.get('cmuitaccount')
        user = User.query.filter_by(email=email).first()
        if user.is_admin == True:
            try:
                #contact = Contact.query.get(id_)
                user = User.query.get(id_)
                if is_null != None:
                        user_entry = user.update(
                    email=None,
                    is_admin=None
                    )
                else:
                    db.session.delete(user)
                db.session.commit()
            except Exception as ex:
                app.logger.debug(ex)
                raise
        else:
            flash("You do not have permission to delete.")
    return home()
