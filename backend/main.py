from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user,login_required,LoginManager,logout_user
from celery import Celery
from flask_bcrypt import check_password_hash, generate_password_hash, Bcrypt
from models import *
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
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
        return Admin.query.get(user_name)
    elif user_type == 'sponsor':
        return Sponsor.query.get(user_name)
    elif user_type == 'influencer':
        return Influencer.query.get(user_name)
    return None

@app.route('/api', methods=['GET'])
def get():
    return jsonify({'msg': 'Hello World'})

@app.route('/')
def index():
    return 'Hello, World!'

@app.route('/login', methods=['POST'])
def login():
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']

        user = None
        if role == 'admin':
            user = Admin.query.filter_by(username=username).first()
        elif role == 'sponsor':
            user = Sponsor.query.filter_by(username=username).first()
        elif role == 'influencer':
            user = Influencer.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user, remember=True, id=f'{role}:{user.username}')
            return {"message":True}
        else:
            return {"message":False}

if __name__ == '__main__':
    app.run(debug=True)