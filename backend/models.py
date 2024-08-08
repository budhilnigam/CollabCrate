# coding: utf-8
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()



class AdRequest(db.Model):
    __tablename__ = 'ad_requests'

    ad_id = db.Column(db.Integer, primary_key=True)
    cmpn_id = db.Column(db.ForeignKey('campaigns.cmpn_id'), nullable=False)
    inf_id = db.Column(db.ForeignKey('influencers.inf_id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    payment_amt = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Text, nullable=False, server_default=db.FetchedValue())

    cmpn = db.relationship('Campaign', primaryjoin='AdRequest.cmpn_id == Campaign.cmpn_id')
    inf = db.relationship('Influencer', primaryjoin='AdRequest.inf_id == Influencer.inf_id')

    def __init__(self, cmpn_id, inf_id, message, payment_amt, status):
        self.cmpn_id = cmpn_id
        self.inf_id = inf_id
        self.message = message
        self.payment_amt = payment_amt
        self.status = status

    



class Admin(db.Model):
    __tablename__ = 'admin'

    username = db.Column(db.Text, primary_key=True, server_default=db.FetchedValue())
    password = db.Column(db.Text, nullable=False)

    def get_id(self):
        return f"admin:{self.username}"



class Campaign(db.Model):
    __tablename__ = 'campaigns'

    cmpn_id = db.Column(db.Integer, primary_key=True)
    cmpn_name = db.Column(db.Text, nullable=False)
    cmpn_description = db.Column(db.Text, nullable=False)
    start_date = db.Column(db.Text, nullable=False)
    end_date = db.Column(db.Text, nullable=False)
    budget = db.Column(db.Integer, nullable=False)
    visibility = db.Column(db.Text, nullable=False, server_default=db.FetchedValue())
    goals = db.Column(db.Text, nullable=False)

    def __init__(self, cmpn_name, cmpn_description, start_date, end_date, budget, visibility, goals):
        self.cmpn_name = cmpn_name
        self.cmpn_description = cmpn_description
        self.start_date = start_date
        self.end_date = end_date
        self.budget = budget
        self.visibility = visibility
        self.goals = goals



class Influencer(db.Model):
    __tablename__ = 'influencers'

    inf_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, nullable=False)
    password = db.Column(db.Text, nullable=False)
    inf_category = db.Column(db.Text, nullable=False)
    inf_niche = db.Column(db.Text, nullable=False)
    inf_reach = db.Column(db.Integer, nullable=False)

    def __init__(self, username, password, inf_category, inf_niche, inf_reach):
        self.username = username
        self.password = password
        self.inf_category = inf_category
        self.inf_niche = inf_niche
        self.inf_reach = inf_reach

    def get_id(self):
        return f"influencer:{self.username}"

class Sponsor(db.Model):
    __tablename__ = 'sponsors'

    sp_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, nullable=False)
    sp_industry = db.Column(db.Text, nullable=False)
    sp_budget = db.Column(db.Integer, nullable=False)
    password = db.Column(db.Text, nullable=False)

    def __init__(self, username, sp_industry, sp_budget, password):
        self.username = username
        self.sp_industry = sp_industry
        self.sp_budget = sp_budget
        self.password = password

    def get_id(self):
        return f"sponsor:{self.username}"