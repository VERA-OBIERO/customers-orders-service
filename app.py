import os
import requests
import pathlib
import cachecontrol
from flask import Flask, abort, redirect, request, session, url_for
import google_auth_oauthlib
from models import db
from flask_migrate import Migrate
from customer import customer_bp, api as customer_api
from order import order_bp, api as order_api
from login import login_is_required
from swagger import swaggerui_bp
from serializers import ma
from google_auth_oauthlib.flow import Flow
#from google.auth.transport import requests
from google.auth.transport.requests import Request
from google.oauth2 import id_token

#from auth import oidc


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///customer_orders.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '234678234'
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
GOOGLE_CLIENT_ID = "1020899568200-4jbe31rg8c441dsdotvh60d0bu58jt7u.apps.googleusercontent.com"
client_secrets_file= os.path.join(pathlib.Path(__file__).parent, "client_secrets.json")
flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri="http://127.0.0.1:5000/callback"
)


# app.config['OIDC_CLIENT_SECRETS'] = 'client_secrets.json'  
# app.config['OIDC_ID_TOKEN_COOKIE_SECURE'] = False   

#oidc.init_app(app)

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
    return "Hello World <a href='/login'><button>login</button></a>"

@app.route('/login')
def login():
    # session["google_id"] = "Test"
    # return redirect("/protected")
    authorization_url, state = flow.authorization_url()
    session["state"] = state 
    return redirect(authorization_url)

@app.route('/callback')
def callback():
    flow.fetch_token(authorization_response=request.url)

    if not session["state"] == request.args["state"]:
        abort(500)

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID
    )
    session["google_id"] = id_info.get("sub")
    session["name"] = id_info.get("name")
    return redirect("/protected")

@app.route('/logout')
def logout():
    session.clear()
    return redirect("/")

@app.route('/protected')
@login_is_required
def protected():
    return "protected <a href='/logout'><button>logout</button></a>"

if __name__ == '__main__':
    app.run(debug=True)
