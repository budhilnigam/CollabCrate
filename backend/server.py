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
from datetime import datetime
import os
import redis
from io import StringIO
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
app.config.enable_utc = False
#app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/1'
#app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/1'
#app.config['CACHE_TYPE'] = 'redis'
#app.config['CACHE_REDIS_URL'] = 'redis://localhost:6379/0'

class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)
def celery_init_app(app: Flask) -> Celery:

    celery_app = Celery(app.import_name, task_cls=FlaskTask)
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
            if j!='_sa_instance_state' and j!='password':
                if r._mapping[j] is not None:
                    result[len(result)-1][j]=r._mapping[j]
                else:
                    result[len(result)-1][j]=""
    return result

@app.route('/api', methods=['GET'])
def get():
    return jsonify({'msg': 'Hello World'})

#@app.route('/')
#def index():
#    send_email_reminder("budhilnigam@gmail.com", 'Daily Reminder', 'Please check your ad requests.')
#    return "Email sent successfully"
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
        email = request.form['email']
        sponsor = sponsors(username=username,email=email, password=bcrypt.generate_password_hash(password),sp_industry=sp_industry,sp_budget=sp_budget)
        db.session.add(sponsor)
        db.session.commit()
        login_user(sponsor)
        return {"message":True}
    elif role == 'influencer':
        if Influencer.query.filter_by(username=username).first():
            return {"message":"Another user already exists with this username"}
        inf_category=request.form['inf_category']
        inf_niche=request.form['inf_niche']
        inf_reach=request.form['inf_reach']
        email = request.form['email']
        influencer = Influencer(username=username,email=email, password=bcrypt.generate_password_hash(password),inf_category=inf_category,inf_niche=inf_niche,inf_reach=inf_reach)
        db.session.add(influencer)
        db.session.commit()
        login_user(influencer)
        return {"message":True}
    elif role == 'admin':
        if Admin.query.filter_by(username=username).first():
            return {"message":"Another user already exists with this username"}
        admin = Admin(username=username,password=bcrypt.generate_password_hash(password))
        db.session.add(admin)
        db.session.commit()
        login_user(admin)
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
        

@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return {"message":True}


@app.route('/get_user', methods=['GET'])
@login_required
def get_user():
    print(singlequeryconverter(current_user))
    return jsonify(singlequeryconverter(current_user))

@celery.task
def send_email_reminder(email, subject, body):
    msg = Message(subject,sender=os.getenv("MAIL_USERNAME"),recipients=[email])
    msg.body = body
    mail.send(msg)
    return "Sent successfully"

@celery.task(name='daily_reminders')
def daily_reminders():
    #send_email_reminder.delay("budhilnigam@gmail.com", 'Daily Reminder', 'Please check your ad requests.')
    for sponsor in db.session.query(sponsors.username,sponsors.email,Campaign.cmpn_name).join(Campaign, sponsors.username==Campaign.sp_username).join(AdRequest, Campaign.cmpn_id==AdRequest.cmpn_id).filter_by(status='pending').all():
        send_email_reminder.delay(sponsor.email, 'Daily Reminder', 'You have got a new ad request for campaign '+sponsor.cmpn_name +'.')

@celery.task(name='send_monthly_report')
def send_monthly_report():
    # Get the current month and year for the report header
    current_month = datetime.now().strftime('%B %Y')

    # Fetch all the sponsors
    sponsors_list = sponsors.query.all()

    # Loop through each sponsor to create a specific report for them
    for sponsor in sponsors_list:
        # Fetch campaigns for the sponsor
        campaigns = Campaign.query.filter_by(sp_username=sponsor.username).all()

        # Create a summary of activities for the report
        report_data = []
        
        for campaign in campaigns:
            # Calculate the number of ads and total payment for each campaign
            ad_requests = AdRequest.query.filter_by(cmpn_id=campaign.cmpn_id).all()
            ads_done = len(ad_requests)
            total_payment = sum([ad_request.payment_amt for ad_request in ad_requests])

            sales_growth = 10

            budget_used = total_payment
            budget_remaining = campaign.budget - budget_used

            report_data.append({
                'campaign_name': campaign.cmpn_name,
                'ads_done': ads_done,
                'total_payment': total_payment,
                'sales_growth': sales_growth,
                'budget_used': budget_used,
                'budget_remaining': budget_remaining
            })

        # Generate the HTML content for the sponsor's email
        html_content = f"""
        <h1>Monthly Activity Report - {current_month}</h1>
        <h2>Campaigns for {sponsor.username}</h2>
        <table border="1" cellpadding="10">
            <tr>
                <th>Campaign Name</th>
                <th>Ads Done</th>
                <th>Total Payment</th>
                <th>Sales Growth (%)</th>
                <th>Budget Used</th>
                <th>Budget Remaining</th>
            </tr>
        """
        
        for data in report_data:
            html_content += f"""
            <tr>
                <td>{data['campaign_name']}</td>
                <td>{data['ads_done']}</td>
                <td>${data['total_payment']}</td>
                <td>{data['sales_growth']}%</td>
                <td>${data['budget_used']}</td>
                <td>${data['budget_remaining']}</td>
            </tr>
            """
        
        html_content += "</table>"

        msg = Message(
            subject=f"Monthly Activity Report - {current_month}",
            sender=os.getenv("MAIL_USERNAME"),
            recipients=[sponsor.email],
            body="Please find your monthly activity report below.",
            html=html_content
        )

        mail.send(msg)

    return "Monthly reports sent successfully"


celery.conf.beat_schedule = {
    'daily-reminders': {
        'task': 'daily_reminders',
        'schedule': crontab(hour=20, minute=13),
    },
    'send-monthly-report': {
        'task': 'send_monthly_report',
        'schedule': crontab(hour=20, minute=14),
    },
}

@app.route('/export_campaigns', methods=['POST'])
@login_required
def export_campaigns():
    export_campaigns_to_csv.delay(current_user.username)
    return {"message":"Export started"}

@celery.task(name='export_campaigns_to_csv')
def export_campaigns_to_csv(sponsor_username):
    from models import Campaign
    import csv
    import os

    # Get the sponsor's data
    sponsor = sponsors.query.filter_by(username=sponsor_username).first()

    # Fetch campaigns for the sponsor
    campaigns = Campaign.query.filter_by(sp_username=sponsor_username).all()

    # Create a CSV in memory using StringIO
    csv_file = StringIO()
    writer = csv.writer(csv_file)
    
    # Write the header
    writer.writerow(['Campaign Name', 'Description', 'Start Date', 'End Date', 'Budget', 'Visibility', 'Goals'])
    
    # Write campaign data
    for campaign in campaigns:
        writer.writerow([campaign.cmpn_name, campaign.cmpn_description, campaign.start_date,
                         campaign.end_date, campaign.budget, campaign.visibility, campaign.goals])
    
    # Reset the pointer to the beginning of the file for reading
    csv_file.seek(0)

    # Create the email message
    msg = Message(
        subject="Campaign Data Export",
        sender=os.getenv("MAIL_USERNAME"),  # Your sender email address
        recipients=[sponsor.email],
        body="Your campaign data has been exported. Please find the CSV file attached."
    )

    # Attach the CSV file to the email
    msg.attach(
        f"{sponsor_username}_campaigns.csv",  # Filename for attachment
        "text/csv",  # MIME type for CSV files
        csv_file.getvalue()  # File contents
    )

    mail.send(msg)

    return "Exported successfully"


def register_routes():
    import ads,campaigns,admin,sponsor,influencer
    
if __name__ == '__main__':
    register_routes()
    app.run(debug=True)