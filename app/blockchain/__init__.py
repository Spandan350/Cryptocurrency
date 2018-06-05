from flask import Flask
app = Flask(__name__)
 
app.secret_key = 'your_secret_key'
 
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USE_TLS"] = False
app.config["MAIL_USERNAME"] = 'assistance.blockchain@gmail.com'
app.config["MAIL_PASSWORD"] = 'secret'
app.config['MAIL_DEFAULT_SENDER'] = 'assistance.blockchain@gmail.com'
app.config["SECURITY_PASSWORD_SALT"]= 'my_precious_two'


app.config["SECRET_KEY"] = 'my_precious'
app.config["DEBUG"] = False
app.config["BCRYPT_LOG_ROUNDS"] = 13
app.config["WTF_CSRF_ENABLED"] = True
app.config["DEBUG_TB_ENABLED"] = False
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

    


from blockchain.routes import mail
mail.init_app(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1234@localhost:3306/blockchain'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
 
from blockchain.models import db
db.init_app(app)


