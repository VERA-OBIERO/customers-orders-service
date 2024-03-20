from flask import Flask, redirect, url_for
from models import db
from flask_migrate import Migrate
from customer import customer_bp, api as customer_api
from order import order_bp, api as order_api
from swagger import swaggerui_bp
from serializers import ma
from auth import oidc

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///customer_orders.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '234678234'
app.config['OIDC_CLIENT_SECRETS'] = 'client_secrets.json'  
app.config['OIDC_ID_TOKEN_COOKIE_SECURE'] = False   

oidc.init_app(app)

db.init_app(app)
ma.init_app(app)
migrate = Migrate(app, db)

customer_api.init_app(customer_bp)
app.register_blueprint(customer_bp)

order_api.init_app(order_bp)
app.register_blueprint(order_bp)

app.register_blueprint(swaggerui_bp, url_prefix="/swagger")

@app.route('/')
def index():
    return 'Hello, World!'

@app.route('/login')
@oidc.require_login
def login():
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    oidc.logout()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
