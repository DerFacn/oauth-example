from flask import Flask, render_template, g, request, redirect, url_for
from authlib.integrations.flask_client import OAuth
from .models import User
from .db import session
from .config import Config


app = Flask(__name__)
app.config.from_object(Config)

CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
oauth = OAuth(app)
oauth.register(
    name='google',
    server_metadata_url=CONF_URL,
    client_kwargs={
        'scope': 'openid email profile'
    }
)


@app.before_request
def before_request():
    user_id = request.cookies.get('user_id')
    g.user = None

    if user_id:
        g.user = session.query(User).filter_by(id=user_id).first()


@app.route('/')
def index():
    return render_template('home.html')


from app import auth

app.register_blueprint(auth.bp)
#
#
# @app.route('/login')
# def login():
#     redirect_uri = url_for('auth', _external=True)
#     return oauth.google.authorize_redirect(redirect_uri)
#
#
# @app.route('/auth/google')
# def auth():
#     token = oauth.google.authorize_access_token()
#     session['user'] = token['userinfo']
#     return redirect('/')
#
#
# @app.route('/logout')
# def logout():
#     session.pop('user', None)
#     return redirect('/')
