from flask_sqlalchemy import SQLAlchemy
from werkzeug import generate_password_hash, check_password_hash
 
db = SQLAlchemy()
 
class User(db.Model):
  __tablename__ = 'Users'
  uid = db.Column('ID',db.Integer, primary_key = True)
  firstname = db.Column('FirstName',db.String(100),nullable=False)
  lastname = db.Column('LastName',db.String(100),nullable=False)
  pwdhash = db.Column('PwdHash',db.String(200),nullable=False)
  phone = db.Column('Phone',db.String(20), unique=True,nullable=False)
  email = db.Column('Email',db.String(200), unique=True,nullable=False)
  balance = db.Column('Balance',db.Float, unique=True,nullable=True)
  hash = db.Column('Hash',db.String(200), unique=True,nullable=False)
   
  def __init__(self, firstname, lastname, email, password, phone, balance, hash):
    self.firstname = firstname.title()
    self.lastname = lastname.title()
    self.email = email.lower()
    self.set_password(password)
    self.phone=phone
    self.balance=balance
    self.hash=hash

  def set_password(self, password):
    self.pwdhash = generate_password_hash(password)

  def check_password(self, password):
    return check_password_hash(self.pwdhash, password)
  
class Trans(db.Model):
  __tablename__ ='Trans'
  tid = db.Column('ID',db.Integer, primary_key = True)
  sender_email = db.Column('SenderEmail',db.String(200),nullable=False)
  receiver_email = db.Column('ReceiverEmail',db.String(200),nullable=False)
  receiver_hash = db.Column('ReceiverHash',db.String(200),nullable=False)
  coinz = db.Column('Coinz',db.Float,nullable=False)
  date = db.Column('Date',db.String(50),nullable=False)

  def __init__(self,sender_email,receiver_email,receiver_hash,coinz,date):
    self.sender_email=sender_email
    self.receiver_email=receiver_email
    self.receiver_hash=receiver_hash
    self.coinz=coinz
    self.date=date

class Buy(db.Model):
  __tablename__='Buy'
  bid=db.Column('ID',db.Integer, primary_key = True)
  email=db.Column('Email',db.String(200),nullable=False)
  coinz=db.Column('Coinz',db.Float,nullable=False)
  inr=db.Column('INR',db.Float,nullable=False)
  date=db.Column('Date',db.String(50),nullable=False)
    
  def __init__(self,email,coinz,inr,date):
    self.email=email
    self.coinz=coinz
    self.inr=inr
    self.date=date

class Sell(db.Model):
  __tablename__='Sell'
  sid=db.Column('ID',db.Integer, primary_key = True)
  email=db.Column('Email',db.String(200),nullable=False)
  coinz=db.Column('Coinz',db.Float,nullable=False)
  inr=db.Column('INR',db.Float,nullable=False)
  date=db.Column('Date',db.String(50),nullable=False)
    
  def __init__(self,email,coinz,inr,date):
    self.email=email
    self.coinz=coinz
    self.inr=inr
    self.date=date

class Bank(db.Model):
  __tablename__ = 'Bank'
  bankid = db.Column('ID',db.Integer, primary_key = True)
  email = db.Column('Email',db.String(200),nullable=False)
  bankname = db.Column('BankName',db.String(200),nullable=False)
  name = db.Column('Name',db.String(200),nullable=False)
  cardno = db.Column('CardNo',db.String(200), unique=True,nullable=False)
  expire = db.Column('Expire',db.String(50),nullable=False)
  ccv = db.Column('CCV',db.String(10),nullable=False)
    
  def __init__(self,email, bankname, name, cardno, expire, ccv):
    self.bankname = bankname.title()
    self.name = name.title()
    self.email = email.lower()
    self.cardno=cardno
    self.expire=expire
    self.ccv=ccv