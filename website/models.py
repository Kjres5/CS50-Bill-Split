from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

#modify to transactions
class Transaction(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
  name = db.Column(db.String(150))
  remarks = db.Column(db.String(150))
  cost = db.Column(db.Numeric)

class User(db.Model, UserMixin): 
  id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.String(150), unique=True)
  password = db.Column(db.String(150))
  first_name = db.Column(db.String(150))
  transactions = db.relationship('Transaction')
  friends = db.Column(db.String(99999))
