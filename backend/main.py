from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user,login_required,LoginManager,logout_user,current_user
from celery import Celery
from flask_bcrypt import check_password_hash, generate_password_hash, Bcrypt
from models import *
import os
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SECRET_KEY'] = 'mysecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///'+ os.path.join(basedir, 'database.db')
app.config['CACHE_TYPE'] = 'redis'
app.config['CACHE_REDIS_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/1'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/1'

cors=CORS(app)
bcrypt=Bcrypt(app)
db.init_app(app)
login_manager=LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user):
    user_type, user_name = user.split(":")
    
    if user_type == 'admin':
        return Admin.query.filter_by(username=user_name).first()
    elif user_type == 'sponsor':
        return sponsors.query.filter_by(username=user_name).first()
    elif user_type == 'influencer':
        return Influencer.query.filter_by(username=user_name).first()
    return None

@app.route('/api', methods=['GET'])
def get():
    return jsonify({'msg': 'Hello World'})

@app.route('/')
def index():
    return 'Hello, World!'

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    role = request.args.get('role')

    if role == 'sponsor':
        if sponsors.query.filter_by(username=username).first():
            return {"message":"Another user already exists with this username"}
        sp_industry=request.form['sp_industry']
        sp_budget=request.form['sp_budget']
        sponsor = sponsors(username=username, password=bcrypt.generate_password_hash(password),sp_industry=sp_industry,sp_budget=sp_budget)
        db.session.add(sponsor)
        db.session.commit()
        return {"message":True}
    elif role == 'influencer':
        if Influencer.query.filter_by(username=username).first():
            return {"message":"Another user already exists with this username"}
        inf_category=request.form['inf_category']
        inf_niche=request.form['inf_niche']
        inf_reach=request.form['inf_reach']
        influencer = Influencer(username=username, password=bcrypt.generate_password_hash(password),inf_category=inf_category,inf_niche=inf_niche,inf_reach=inf_reach)
        db.session.add(influencer)
        db.session.commit()
        return {"message":True}

@app.route('/login', methods=['POST'])
def login():
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']

        user = None
        if role == 'admin':
            user = Admin.query.filter_by(username=username).first()
        elif role == 'sponsor':
            user = sponsors.query.filter_by(username=username).first()
        elif role == 'influencer':
            user = Influencer.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return {"message":True}
        else:
            return {"message":False}
        

@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return {"message":True}

import ads
if __name__ == '__main__':
    app.run(debug=True)