from flask_wtf import Form
from wtforms.validators import ValidationError
from wtforms import TextField, BooleanField, PasswordField, TextAreaField, validators, SubmitField, DecimalField
from blockchain.models import db, User


class ContactForm(Form):
  name = TextField("Name",  [validators.Required("Please enter your name.")])
  email = TextField("Email",  [validators.Required("Please enter your email address."), validators.Email("Please enter your email address.")])
  subject = TextField("Subject",  [validators.Required("Please enter a subject.")])
  message = TextAreaField("Message",  [validators.Required("Please enter a message.")])
  submit = SubmitField("Send")
  

class SignupForm(Form):
  firstname = TextField("First name",  [validators.Required("required")])
  lastname = TextField("Last name",  [validators.Required("required")])
  email = TextField("Email",  [validators.Required("required"), validators.Email("required")])
  password = PasswordField('Password', [validators.Required("required")])
  phone = TextField('Mobile Number', [validators.Required("required"),validators.Length(min=10, max=10,message="Mobile Number should be 10 digits long")])
  submit = SubmitField("Create account")
 
  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)
 
  def validate(self):
    if not Form.validate(self):
      return False
     
    user = User.query.filter_by(email = self.email.data.lower()).first()
    if user:
      self.email.errors.append("That email is already taken")
      return False
    else:
      ph= User.query.filter_by(phone = self.phone.data).first()
      if ph:
        self.phone.errors.append("That phone is already registered")
        return False
      return True

class SigninForm(Form):
  email = TextField("Email",  [validators.Required("required"), validators.Email("required")])
  password = PasswordField('Password', [validators.Required("required")])
  submit = SubmitField("Sign In")
   
  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)
 
  def validate(self):
    if not Form.validate(self):
      return False
     
    user = User.query.filter_by(email = self.email.data.lower()).first()
    if user and user.check_password(self.password.data):
      return True
    else:
      self.email.errors.append("Invalid e-mail or password")
      return False	  

class PurchaseForm(Form):
  coinz= DecimalField("CNZ:",  [validators.Required("Please enter number of coinz.")])
  inr= DecimalField("INR:",  [validators.Required("Please enter INR.")])
  if not inr:
    inr = coinz / 10
  if not coinz:
    coinz = inr * 10
  submit = SubmitField("BUY")
  def validate(self):
    if not Form.validate(self):
      return False
    else:
      return True

class SaleForm(Form):
  coinz= TextField("CNZ:",  [validators.Required("Please enter either coinz or INR.")])
  inr= TextField("INR:",  [validators.Required("Please either coinz or INR.")])
  submit = SubmitField("SELL")
  def validate(self):
    if not Form.validate(self):
      return False
    else:
      return True	

class MineForm(Form):
  mine= TextField("Mine Coinz",  [validators.Required("Please enter amount to be mined.")])
  submit = SubmitField("MINE")
  def validate(self):
    if not Form.validate(self):
      return False
    else:
      return True

class ChangeHashForm(Form):
  submit = SubmitField("CHANGE HASH")
  def validate(self):
    if not Form.validate(self):
      return False
    else:
      return True	



class BankForm(Form):
  bankname=TextField("Name of Bank",  [validators.Required("Please enter bank name")])
  name=TextField("Name on card",  [validators.Required("Please enter name.")])
  cardno=TextField("Card Number",  [validators.Required("Please enter card number."),validators.Length(min=16, max=19),validators.Regexp('^(?:4[0-9]{12}(?:[0-9]{3})?|(?:5[1-5][0-9]{2}| 222[1-9]|22[3-9][0-9]|2[3-6][0-9]{2}|27[01][0-9]|2720)[0-9]{12}|3[47][0-9]{13}|3(?:0[0-5]|[68][0-9])[0-9]{11}|6(?:011|5[0-9]{2})[0-9]{12}|(?:2131|1800|35\d{3})\d{11})$', message="Not a Credit/Debit card number")])
  expire=TextField("Expiry Date",  [validators.Required("Please enter expire."),validators.Regexp('^((1)([0-2]{1})|[1-9]{2})[/]20([0-9]{2})$', message="Enter date in format MM/20YY")])
  ccv=TextField("Security Number",  [validators.Required("Please enter security code."),validators.Length(min=3, max=3,message="The ccv must be of length 3")])
  def validate(self):
    if not Form.validate(self):
      return False
    else:
      return True 
              
	  
	  
class PaymentForm(Form):
  #sender = TextField("First name",  [validators.Required("Please enter your first name.")])
  recipient = TextField("Recipient Hash:",  [validators.Required("Please enter the recipient.")])
  amount = TextField("Number of Coinz",  [validators.Required("Please enter the number of coinz(might be decimal).")])
  submit = SubmitField("Pay")
  
  def validate(self):
    if not Form.validate(self):
      return False
     
    #user = User.query.filter_by(hash = self.recipient.data.lower()).first()
    #if not user:
    #  self.recipient.errors.append("No such recipient exist")
    #  return False
    else:
	  #u = User.query.filter_by(email = session['email']).first()
      #if u.balance < self.amount.data:
      #  self.amount.errors.append("Sorry! Account balance insufficient. Why don't you buy some coinz.")
      #  return False
      return True