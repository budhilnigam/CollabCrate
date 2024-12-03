# models.py
from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin

db = SQLAlchemy()

class AdRequest(db.Model):
    __tablename__ = 'ad_requests'

    ad_id = db.Column(db.Integer, primary_key=True)
    cmpn_id = db.Column(db.ForeignKey('campaigns.cmpn_id'), nullable=False)
    inf_id = db.Column(db.ForeignKey('influencers.inf_id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    payment_amt = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Text, nullable=False, server_default=db.FetchedValue())
    made_by = db.Column(db.Text, nullable=False)
    
    cmpn = db.relationship('Campaign', primaryjoin='AdRequest.cmpn_id == Campaign.cmpn_id')
    inf = db.relationship('Influencer', primaryjoin='AdRequest.inf_id == Influencer.inf_id')

    def __init__(self, cmpn_id, inf_id, message, payment_amt, status='pending',made_by='sponsor'):
        self.cmpn_id = cmpn_id
        self.inf_id = inf_id
        self.message = message
        self.payment_amt = payment_amt
        self.status = status
        self.made_by = made_by


class Admin(db.Model, UserMixin):
    __tablename__ = 'admin'

    username = db.Column(db.Text, primary_key=True, server_default=db.FetchedValue())
    password = db.Column(db.Text, nullable=False)

    def get_id(self):
        return f"admin:{self.username}"
    
    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True



class Campaign(db.Model):
    __tablename__ = 'campaigns'

    cmpn_id = db.Column(db.Integer, primary_key=True)
    cmpn_name = db.Column(db.Text, nullable=False)
    sp_username=db.Column(db.ForeignKey('sponsors.username'), nullable=False)
    cmpn_description = db.Column(db.Text, nullable=False)
    start_date = db.Column(db.Text, nullable=False)
    end_date = db.Column(db.Text, nullable=False)
    budget = db.Column(db.Integer, nullable=False)
    visibility = db.Column(db.Text, nullable=False, server_default=db.FetchedValue())
    goals = db.Column(db.Text, nullable=False)
    flagged = db.Column(db.Boolean, nullable=False, server_default=db.FetchedValue())
    def __init__(self, cmpn_name, sp_username, cmpn_description, start_date, end_date, budget, goals,visibility='private'):
        self.cmpn_name = cmpn_name
        self.cmpn_description = cmpn_description
        self.sp_username = sp_username
        self.start_date = start_date
        self.end_date = end_date
        self.budget = budget
        self.visibility = visibility
        self.goals = goals



class Influencer(db.Model, UserMixin):
    __tablename__ = 'influencers'

    inf_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, nullable=False)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, nullable=False)
    inf_category = db.Column(db.Text, nullable=False)
    inf_niche = db.Column(db.Text, nullable=False)
    inf_reach = db.Column(db.Integer, nullable=False)
    approved = db.Column(db.Boolean, nullable=False, server_default=db.FetchedValue())
    flagged = db.Column(db.Boolean, nullable=False, server_default=db.FetchedValue())
    def __init__(self, username, password, email, inf_category, inf_niche, inf_reach):
        self.username = username
        self.password = password
        self.email = email
        self.inf_category = inf_category
        self.inf_niche = inf_niche
        self.inf_reach = inf_reach

    def get_id(self):
        return f"influencer:{self.username}"
    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True
    

class sponsors(db.Model):
    __tablename__ = 'sponsors'
    sp_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, nullable=False)
    sp_industry = db.Column(db.Text, nullable=False)
    sp_budget = db.Column(db.Integer, nullable=False)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, nullable=False)
    approved = db.Column(db.Boolean, nullable=False, server_default=db.FetchedValue())
    flagged = db.Column(db.Boolean, nullable=False, server_default=db.FetchedValue())
    def __init__(self, username, email, sp_industry, sp_budget, password):
        self.username = username
        self.email = email
        self.sp_industry = sp_industry
        self.sp_budget = sp_budget
        self.password = password

    def get_id(self):
        return f"sponsor:{self.username}"
    
    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True

"""class adrooms(db.Model):
    __tablename__ = 'adrooms'
    room_id = db.Column(db.Integer, primary_key=True)
    cmpn_id = db.Column(db.Integer, nullable=False)
    inf_id = db.Column(db.Integer, nullable=False)
    room = db.Column(db.Text, nullable=False)
    flagged = db.Column(db.Boolean, nullable=False, server_default=db.FetchedValue())
    def __init__(self, cmpn_id, inf_id, room):
        self.cmpn_id = cmpn_id
        self.inf_id = inf_id
        self.room = room"""
"""class chats(db.Model):
    __tablename__ = 'chats'
    chat_id = db.Column(db.Integer, primary_key=True)
    cmpn_id = db.Column(db.Integer, nullable=False)
    inf_id = db.Column(db.Integer, nullable=False)
    chat = db.Column(db.Text, nullable=False)
    flagged = db.Column(db.Boolean, nullable=False, server_default=db.FetchedValue())
    def __init__(self, cmpn_id, inf_id, chat):
        self.cmpn_id = cmpn_id
        self.inf_id = inf_id
        self.chat = chat"""

