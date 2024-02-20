from flask import Flask
from models import db
from flask_migrate import Migrate
from blueprints.customer import customer_bp, api as customer_api
from blueprints.order import order_bp, api as order_api
from serializers import ma

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///customer_orders.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
ma.init_app(app)
migrate = Migrate(app, db)

customer_api.init_app(customer_bp)
app.register_blueprint(customer_bp)

order_api.init_app(order_bp)
app.register_blueprint(order_bp)

@app.route('/')
def index():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(debug=True)
