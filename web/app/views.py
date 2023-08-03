from flask import (jsonify, render_template,request, url_for, flash, redirect)
import json

from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.urls import url_parse
from sqlalchemy.sql import text
# from flask_login import login_user, login_required, logout_user , current_user

from app import app
from app import db
# from app import login_manager


from app.models.authuser import AuthUser

# @login_manager.user_loader
# def load_user(user_id):
#     # since the user_id is just the primary key of our
#     # user table, use it in the query for the user
#     return AuthUser.query.get(int(user_id))

@app.route('/')
def home():
    return render_template("project/index.html")

@app.route('/form')
def form():
    return render_template("project/form.html")

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


# @app.route('/dashboard')
# def dashboard():
#     return 