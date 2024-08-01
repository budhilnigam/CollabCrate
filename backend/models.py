from sqlalchemy import Column, Integer, String
from __main__ import db
class User(db.Model):
    username=String()
    password=String()