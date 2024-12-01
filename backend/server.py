#Server.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user,login_required,LoginManager,logout_user,current_user
from flask_mail import Mail,Message
from flask_bcrypt import check_password_hash, generate_password_hash, Bcrypt
from flask_caching import Cache
from models import *
from celery import Celery,Task
from celery.schedules import crontab
import os
import redis
from dotenv import load_dotenv
celery=None
load_dotenv()
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SECRET_KEY'] = 'mysecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///'+ os.path.join(basedir, 'database.db')
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['CACHE_TYPE'] = 'redis'
app.config['CACHE_REDIS_HOST'] = 'localhost'
app.config['CACHE_REDIS_PORT'] = 6379
app.config['CACHE_REDIS_DB'] = 0
app.config['CACHE_DEFAULT_TIMEOUT'] = 360
app.config.from_mapping(
    CELERY=dict(
        broker_url='redis://localhost:6379/1',
        result_backend='redis://localhost:6379/1',
        task_ignore_result=True,
    ),
)

#app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/1'
#app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/1'
#app.config['CACHE_TYPE'] = 'redis'
#app.config['CACHE_REDIS_URL'] = 'redis://localhost:6379/0'

class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)
def celery_init_app(app: Flask) -> Celery:

    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.config_from_object(app.config["CELERY"])
    celery_app.set_default()
    app.extensions["celery"] = celery_app
    class ContextTask(Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)
    return celery_app

cache=Cache(app)
cache.init_app(app)
redis_client = redis.Redis(host='localhost', port=6379, db=0)
mail=Mail(app)
CORS(app, supports_credentials=True, resources={r"/*": {"origins": "http://localhost:5173"}})
bcrypt=Bcrypt(app)
db.init_app(app)
celery=celery_init_app(app)
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

def queryconverter(query):
    result=[]
    for i in query:
        result.append({})
        for j in i.__dict__:
            if j!='_sa_instance_state' and j!='password':
                result[len(result)-1][j]=i.__dict__[j]
    return result

def singlequeryconverter(query):
    result={}
    for j in query.__dict__:
            if j!='_sa_instance_state' and j!='password':
                result[j]=query.__dict__[j]
    return result

def dbqueryconverter(query):
    result=[]
    for r in query:
        result.append({})
        for j in r._mapping:
            result[len(result)-1][j]=r._mapping[j]
    return result

@app.route('/api', methods=['GET'])
def get():
    return jsonify({'msg': 'Hello World'})

@app.route('/')
def index():
    send_email_reminder("budhilnigam@gmail.com", 'Daily Reminder', 'Please check your ad requests.')
    return "Email sent successfully"
@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    email=request.form['email']
    role = request.args.get('role')

    if role == 'sponsor':
        if sponsors.query.filter_by(username=username).first():
            return {"message":"Another user already exists with this username"}
        sp_industry=request.form['sp_industry']
        sp_budget=request.form['sp_budget']
        sponsor = sponsors(username=username,email=email, password=bcrypt.generate_password_hash(password),sp_industry=sp_industry,sp_budget=sp_budget)
        db.session.add(sponsor)
        db.session.commit()
        return {"message":True}
    elif role == 'influencer':
        if Influencer.query.filter_by(username=username).first():
            return {"message":"Another user already exists with this username"}
        inf_category=request.form['inf_category']
        inf_niche=request.form['inf_niche']
        inf_reach=request.form['inf_reach']
        influencer = Influencer(username=username,email=email, password=bcrypt.generate_password_hash(password),inf_category=inf_category,inf_niche=inf_niche,inf_reach=inf_reach)
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


@app.route('/get_user', methods=['GET'])
@login_required
def get_user():
    print(singlequeryconverter(current_user))
    return jsonify(singlequeryconverter(current_user))
import ads,campaigns,admin

@celery.task
def send_email_reminder(email, subject, body):
    msg = Message(subject,sender=os.getenv("MAIL_USERNAME"),recipients=[email])
    msg.body = body
    mail.send(msg)
    return "Sent successfully"

@celery.task(name='daily_reminders')
def daily_reminders():
    send_email_reminder.delay("budhilnigam@gmail.com", 'Daily Reminder', 'Please check your ad requests.')
    #influencers = db.session.query(Influencer).join(AdRequest, AdRequest.inf_id == Influencer.inf_id).filter(AdRequest.made_by == 'sponsor', AdRequest.status == 'Pending').all()
    #for influencer in dbqueryconverter(influencers):
    #    send_email_reminder.delay("budhilnigam@gmail.com", 'Daily Reminder', 'Please check your ad requests.')

celery.conf.beat_schedule = {
    'daily-reminders': {
        'task': 'daily_reminders',
        'schedule': crontab(hour=10, minute=23),  # Send at 5 PM every day
    },
}

"""@celery.task
def generate_report():"""
    
    
if __name__ == '__main__':
    app.run(debug=True)