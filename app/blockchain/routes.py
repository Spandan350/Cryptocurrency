from flask import Flask, render_template, request, flash, session, url_for, redirect
from blockchain import app
from blockchain.forms import ContactForm, SignupForm, SigninForm, PaymentForm,PurchaseForm, SaleForm, ChangeHashForm,MineForm,BankForm
from flask_mail import Message, Mail
from blockchain.models import db, User, Sell, Buy, Trans,Bank
from blockchain.blockchain import Blockchain
import random
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
#from blockchain.confirm import generate_confirmation_token, confirm_token
from uuid import uuid4
import hashlib
import json
from time import time
from urllib.parse import urlparse
from uuid import uuid4
from datetime import datetime,timedelta
import requests
from flask import Flask, jsonify, request
from sqlalchemy.sql import func

mail = Mail()

#admin can view the whole chain, can mine coinz,admin cannot buy, admin cannot sell,can verify a transaction,cannot accept payments,can view total number of coinz in circulation,reply to message from user,view message from user

# Generate a globally unique address for this node
#node_identifier = str(uuid4()).replace('-', '')

# Instantiate the Blockchain
blockchain = Blockchain()

@app.route('/', methods=['GET', 'POST'])
def home():
  form = ContactForm()
  if request.method=='GET':
    return render_template('home.html',form=form)
  elif request.method=='POST':
    if form.validate() == False:
      flash('All fields are required.')
      redirect(url_for('home'))
      #return render_template('home.html', form=form)
    else:
      msg = Message(form.subject.data,sender='assistance.blockchain@gmail.com',recipients=['spandanghosh350@gmail.com'])
      msg.body = """From: %s <%s> %s """ % (form.name.data, form.email.data, form.message.data)
      mail.send(msg)
      redirect(url_for('home'))
      #return render_template('home.html', success=True)

@app.route('/home', methods=['GET', 'POST'])
def home2():
  form = ContactForm()
  if request.method=='GET':
    return render_template('home.html',form=form)
  elif request.method=='POST':
    if form.validate() == False:
      flash('All fields are required.')
      redirect(url_for('home'))
      #return render_template('home.html', form=form)
    else:
      msg = Message(form.subject.data,sender='assistance.blockchain@gmail.com',recipients=['spandanghosh350@gmail.com'])
      msg.body = """From: %s <%s> %s """ % (form.name.data, form.email.data, form.message.data)
      mail.send(msg)
      redirect(url_for('home'))
      #return render_template('home.html', success=True)   

@app.route('/convert')
def convert():
  return render_template('convert.html')

@app.route('/viewdetails')
def viewdetails():
  bank_det=Bank.query.filter_by(email=session['email']).first()
  return render_template('viewdetails.html',bank_det=bank_det)

@app.route('/changedetails', methods=['GET', 'POST'])
def changedetails():
  form=BankForm()
  if request.method=='GET':
    return render_template('changedetails.html',form=form)
  elif request.method=='POST':
    if form.validate() == False:
      return render_template('changedetails.html', form=form,refill=True)
      #check for duplicate card
    exist= Bank.query.filter_by(email=session['email']).first()
    if exist:
      exist.bankname=form.bankname.data
      exist.name=form.name.data
      exist.cardno=form.cardno.data
      exist.expire=form.expire.data
      exist.ccv=form.ccv.data
      db.session.commit() 
    else:
      update = Bank.query.filter_by(cardno=form.cardno.data).first()
      if update:
        return render_template('changedetails.html',duplicate=True)
      newcard = Bank(session['email'],form.bankname.data, form.name.data, form.cardno.data ,form.expire.data,form.ccv.data,)
      db.session.add(newcard)
      db.session.commit()      
    return render_template('changedetails.html',form=form,bankdet=True)



@app.route('/about')
def about():
  return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
  form = ContactForm()

  if request.method == 'POST':
    if form.validate() == False:
      flash('All fields are required.')
      return render_template('contact.html', form=form)
    else:
      msg = Message(form.subject.data,sender='assistance.blockchain@gmail.com',recipients=['spandanghosh350@gmail.com'])
      msg.body = """From: %s <%s> %s """ % (form.name.data, form.email.data, form.message.data)
      mail.send(msg)
      return render_template('contact.html', success=True)
  elif request.method == 'GET':
    return render_template('contact.html', form=form)

@app.route('/testdb')
def testdb():
  if db.session.query("1").from_statement("SELECT 1").all():
    return 'It works.'
  else:
    return 'Something is broken.'
  
@app.route('/signup', methods=['GET', 'POST'])
def signup():
  form = SignupForm()
  if 'email' in session:
    return redirect(url_for('profile')) 
  if request.method == 'POST':
    if form.validate() == False:
      return render_template('signup.html', form=form)
    else:
      h = str(uuid4()).replace('-','')
      update = User.query.filter_by(hash=h).first()
      while update:
        h=str(uuid4()).replace('-','')
        update = User.query.filter_by(hash=h).first()
      newuser = User(form.firstname.data, form.lastname.data, form.email.data, form.password.data ,form.phone.data,0,h)
      db.session.add(newuser)
      db.session.commit()
      session['email'] = newuser.email
      html = render_template('activate.html')
      msg = Message('THANKS FOR JOINING COINZ!!',html=html,sender='assistance.blockchain@gmail.com',recipients=[newuser.email])
      msg.body = """Welcome %s,<br><br> Your Email id<%s> is registered.""" % (form.firstname.data, form.email.data)
      mail.send(msg)
      return redirect(url_for('profile'))
  elif request.method == 'GET':
    return render_template('signup.html', form=form)
  
  
@app.route('/profile', methods=['GET', 'POST'])
def profile():
  form = ChangeHashForm()
  if 'email' not in session:
    return redirect(url_for('signin'))
  if request.method == 'GET':
    user = User.query.filter_by(email = session['email']).first()
    session['balance']=user.balance
    session['hash']=user.hash
    rcvd_h=Trans.query.filter_by(receiver_email=session['email'])
    #paid=Trans.query.filter_by(sender_email=session['email'])
    pay=3
    
    if user is None:
      return redirect(url_for('signin'))
    else:
      return render_template('profile.html',new=False,form=form,rcvd_h=rcvd_h,firstname=user.firstname,lastname=user.lastname,phone=user.phone,net=user.balance*10,pay=pay)
  elif request.method == 'POST':
    h = str(uuid4()).replace('-','')
    update = User.query.filter_by(hash=h).first()
    while update:
      h=str(uuid4()).replace('-','')
      update = User.query.filter_by(hash=h).first()
    user = User.query.filter_by(email = session['email']).first()
    user.hash=h
    session['hash']=user.hash
    db.session.commit()
    return render_template('profile.html',new=True ,form=form,firstname=user.firstname,lastname=user.lastname,phone=user.phone,net=user.balance*10)
  

@app.route('/admin', methods=['GET', 'POST'])
def admin():
  form=MineForm()
  if 'email' not in session:
    session['email']='assistance.blockchain@gmail.com'
  elif request.method == 'GET':
    blockchain.register_node('http://127.0.0.1:5000')
    user_h=User.query.filter(User.email != 'assistance.blockchain@gmail.com').all()
    trans_h=Trans.query.all();
    sell_h=Sell.query.all()
    buy_h=Buy.query.all()
    mined=db.session.query(func.sum(User.balance).label('mined')).scalar()
    users=db.session.query(func.count(User.balance).label('users')).scalar() - 1
    trans=db.session.query(func.count(Trans.tid).label('trans')).scalar()
    admin_bal=User.query.filter_by(email='assistance.blockchain@gmail.com').first().balance
    return render_template('admin.html', firstname='Administrator',lastname='Spandan',phone=8013873477,user_h=user_h,trans_h=trans_h,buy_h=buy_h,sell_h=sell_h,mined=mined,users=users,trans=trans,admin_bal=admin_bal,form=form)
  elif request.method=='POST':
    last_block = blockchain.last_block
    proof = blockchain.proof_of_work(last_block)
    user = User.query.filter_by(email = session['email']).first()
    # We must receive a reward for finding the proof.
    # The sender is "0" to signify that this node has mined a new coin.
    blockchain.new_transaction(
        sender="0",
        recipient=user.hash,
        amount=float(form.mine.data),
    )

    # Forge the new Block by adding it to the chain
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)

    user.balance=user.balance+float(form.mine.data)
    db.session.commit()
    user_h=User.query.filter(User.email != 'assistance.blockchain@gmail.com').all()
    trans_h=Trans.query.all();
    sell_h=Sell.query.all()
    buy_h=Buy.query.all()
    mined=db.session.query(func.sum(User.balance).label('mined')).scalar()
    users=db.session.query(func.count(User.balance).label('users')).scalar() - 1
    trans=db.session.query(func.count(Trans.tid).label('trans')).scalar()
    admin_bal=User.query.filter_by(email='assistance.blockchain@gmail.com').first().balance
    return render_template('admin.html',mine=True,cnz=form.mine.data,form=form, firstname='Administrator',lastname='Spandan',phone=8013873477,user_h=user_h,trans_h=trans_h,buy_h=buy_h,sell_h=sell_h,mined=mined,users=users,trans=trans,admin_bal=admin_bal)



@app.route('/signin', methods=['GET', 'POST'])
def signin():
  form = SigninForm()
  if 'email' in session:
    return redirect(url_for('profile')) 
  if request.method == 'POST':
    if form.validate() == False:
      return render_template('signin.html', form=form)
    else:
      if form.email.data=='assistance.blockchain@gmail.com':
        session['email']='assistance.blockchain@gmail.com'
        return redirect(url_for('admin'))
      else:
        session['email'] = form.email.data
        return redirect(url_for('profile'))
                 
  elif request.method == 'GET':
    return render_template('signin.html', form=form)

@app.route('/forget', methods=['GET','POST'])
def forget():
  if request.method == 'GET':
    return render_template('forget.html')
  elif request.method == 'POST':
    return render_template('forget.html')

  
@app.route('/pay', methods=['GET', 'POST'])
def pay():
  form = PaymentForm()
  if 'email' not in session:
    return redirect(url_for('profile')) 
  if request.method == 'POST':
    if form.validate() == False:
      return render_template('pay.html', form=form)
    else:
      p = User.query.filter_by(email = session['email']).first()
      if (p.balance >= float(form.amount.data)):
        p.balance=p.balance-float(form.amount.data)
        u=User.query.filter_by(hash=form.recipient.data).first()
        u.balance=u.balance+float(form.amount.data)
        if u.email=='assistance.blockchain@gmail.com':
          return render_template('pay.html',admin=True,form=form)
        t=Trans(p.email,u.email,u.hash,float(form.amount.data),str(datetime.now()))
        db.session.add(t)

        db.session.commit()
        index = blockchain.new_transaction(p.hash, form.recipient.data, str(form.amount.data))
        last_block = blockchain.last_block
        proof = blockchain.proof_of_work(last_block)
        # Forge the new Block by adding it to the chain
        previous_hash = blockchain.hash(last_block)
        block = blockchain.new_block(proof, previous_hash)
        session['balance']=float(session['balance'])-float(form.amount.data)
        with open(r'D:\DESKTOP\flaskapp\app\blockchain\static\json\chain.json',"w") as f:
          f.write(json.dumps(blockchain.chain,sort_keys=True, indent=4))
        return render_template('pay.html',success=True,form=form)
      else:
        return render_template('pay.html',insufficient=True,form=form)    
  elif request.method == 'GET':
    #user = User.query.filter_by(email = session['email'] .lower()).first()
    #trans_h=Trans.query.filter_by(sender_email=session['email'])
    return render_template('pay.html', form=form)
  
@app.route('/payhistory', methods=['GET'])  
def payhistory():
  if 'email' not in session:
    return redirect(url_for('profile')) 
  if request.method == 'GET':
    trans_h=Trans.query.filter_by(sender_email=session['email'])
    return render_template('payhistory.html', trans_h=trans_h)    
  
@app.route('/buy', methods=['GET', 'POST'])
def buy():
  form = PurchaseForm()
  if 'email' not in session:
    return redirect(url_for('profile')) 
  if request.method == 'POST':
    if form.validate() == False:
      return render_template('buy.html', form=form)
    else:
      update = User.query.filter_by(email = session['email']).first()
      update.balance=update.balance+float(form.coinz.data)
      admin=User.query.filter_by(email = 'assistance.blockchain@gmail.com').first()
      admin_hash=admin.hash
      #buy from admin whatever is available else mine
      if form.coinz.data >= admin.balance:
        if admin.balance != 0:
          index = blockchain.new_transaction(admin_hash,update.hash, str(admin.balance))
        temp=float(form.coinz.data)-admin.balance
        admin.balance=0
        if temp>0:
          
          #user = User.query.filter_by(email = session['email']).first()
          # We must receive a reward for finding the proof.
          # The sender is "0" to signify that this node has mined a new coin.
          blockchain.new_transaction(
              sender="0",
              recipient=update.hash,
              amount=str(temp),
          )

          
      else:
        admin.balance=admin.balance-float(form.coinz.data)
        index = blockchain.new_transaction(admin_hash,update.hash, str(form.coinz.data))#sender,recipient
      last_block = blockchain.last_block
      proof = blockchain.proof_of_work(last_block)
      # Forge the new Block by adding it to the chain
      previous_hash = blockchain.hash(last_block)
      block = blockchain.new_block(proof, previous_hash)
      session['balance']=float(session['balance'])+float(form.coinz.data)

      b=Buy(session['email'],float(form.coinz.data),float(form.inr.data),str(datetime.now()))
      db.session.add(b)
      


      db.session.commit()
      with open(r'D:\DESKTOP\flaskapp\app\blockchain\static\json\chain.json',"w") as f:
        f.write(json.dumps(blockchain.chain,sort_keys=True, indent=4))
      
      return render_template('buy.html',success=True,form=form)
  elif request.method == 'GET':
    #buy_h=Buy.query.filter_by(email=session['email'])
    bank=Bank.query.filter_by(email=session['email']).first()
    if not bank:
      return render_template('buy.html',bank=True)
    else:
      return render_template('buy.html', form=form)


@app.route('/buyhistory', methods=['GET'])  
def buyhistory():
  if 'email' not in session:
    return redirect(url_for('profile')) 
  if request.method == 'GET':
    buy_h=Buy.query.filter_by(email=session['email'])
    return render_template('buyhistory.html',buy_h=buy_h)  
  
  
@app.route('/sell', methods=['GET', 'POST'])
def sell():
  form = SaleForm()
  if 'email' not in session:
    return redirect(url_for('profile')) 
  if request.method == 'POST':
    if form.validate() == False:
      return render_template('sell.html', form=form)
    else:
      update = User.query.filter_by(email = session['email']).first()
      admin=User.query.filter_by(email = 'assistance.blockchain@gmail.com').first()
      admin_hash=admin.hash
      if (update.balance >= float(form.coinz.data)):
        update.balance=update.balance-float(form.coinz.data)
        admin.balance=admin.balance + float(form.coinz.data)#actually debit it to admin account
        
        s=Sell(session['email'],float(form.coinz.data),float(form.inr.data),str(datetime.now()))
        db.session.add(s)

        db.session.commit()
        index = blockchain.new_transaction(update.hash,admin_hash,str(form.coinz.data))
        last_block = blockchain.last_block
        proof = blockchain.proof_of_work(last_block)
        # Forge the new Block by adding it to the chain
        previous_hash = blockchain.hash(last_block)
        block = blockchain.new_block(proof, previous_hash)
        session['balance']=float(session['balance'])-float(form.coinz.data)
        with open(r'D:\DESKTOP\flaskapp\app\blockchain\static\json\chain.json',"w") as f:
          f.write(json.dumps(blockchain.chain,sort_keys=True, indent=4))
        return render_template('sell.html',success=True,form=form,money=float(form.coinz.data)*10)
      else:
        return render_template('sell.html',insufficient=True,form=form)                 
  elif request.method == 'GET':
    #sell_h=Sell.query.filter_by(email=session['email'])
    bank=Bank.query.filter_by(email=session['email']).first()
    if not bank:
      return render_template('sell.html',bank=True)
    else:
      return render_template('sell.html', form=form)


@app.route('/sellhistory', methods=['GET'])  
def sellhistory():
  if 'email' not in session:
    return redirect(url_for('profile')) 
  if request.method == 'GET':
    sell_h=Sell.query.filter_by(email=session['email'])
    return render_template('sellhistory.html',sell_h=sell_h)
  
  
@app.route('/signout')
def signout():
 
  if 'email' not in session:
    return redirect(url_for('signin'))
     
  session.pop('email', None)
  return redirect(url_for('home'))
  
  
@app.route('/mine', methods=['GET'])
def mine():
    # We run the proof of work algorithm to get the next proof...
    last_block = blockchain.last_block
    proof = blockchain.proof_of_work(last_block)
    user = User.query.filter_by(email = session['email']).first()
    # We must receive a reward for finding the proof.
    # The sender is "0" to signify that this node has mined a new coin.
    blockchain.new_transaction(
        sender="0",
        recipient=user.hash,
        amount=1,
    )

    # Forge the new Block by adding it to the chain
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)

    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }
    return jsonify(response), 200


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()

    # Check that the required fields are in the POST'ed data
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing values', 400

    # Create a new Transaction
    index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])

    response = {'message': f'Transaction will be added to Block {index}'}
    return jsonify(response), 201


@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200


@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    values = request.get_json()

    nodes = values.get('nodes')
    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400

    for node in nodes:
        blockchain.register_node(node)

    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(blockchain.nodes),
    }
    return jsonify(response), 201


@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    replaced = blockchain.resolve_conflicts()

    if replaced:
        response = {
            'message': 'Our chain was replaced',
            'new_chain': blockchain.chain
        }
    else:
        response = {
            'message': 'Our chain is authoritative',
            'chain': blockchain.chain
        }

    return jsonify(response), 200