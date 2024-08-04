from sqlalchemy import Column, Integer, String
from __main__ import db
class User(db.Model):
    username=String()
    password=String()
    role=String()

    def __init__(self, username, password, role):
        self.username = username
        self.password = password
        self.role = role

class Sponsor(db.Model):
    sp_name=String()
    sp_industry=String()
    sp_budget=Integer()
    role=String()

    def __init__(self, sp_name, sp_industry, sp_budget):
        self.sp_name = sp_name
        self.sp_industry = sp_industry
        self.sp_budget = sp_budget
        

class Influencer(db.Model):
    inf_name=String()
    inf_category=String()
    inf_niche=Integer()
    inf_reach=Integer()

    def __init__(self, inf_name, inf_category, inf_niche, inf_reach):
        self.inf_name = inf_name
        self.inf_category = inf_category
        self.inf_niche = inf_niche
        self.inf_reach = inf_reach

class Campaign(db.Model):
    camp_name=String()
    camp_budget=Integer()
    camp_date=String()
    camp_status=String()

    def __init__(self, camp_name, camp_budget, camp_date, camp_status):
        self.camp_name = camp_name
        self.camp_budget = camp_budget
        self.camp_date = camp_date
        self.camp_status = camp_status