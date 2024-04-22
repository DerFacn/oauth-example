from flask import Blueprint
from .routes import signup, google_oauth, google_auth, add_username, logout, login

bp = Blueprint('auth', __name__, url_prefix='/auth')

bp.add_url_rule('/login', 'login', login, methods=['GET', 'POST'])
bp.add_url_rule('/signup', 'signup', signup, methods=['GET', 'POST'])
bp.add_url_rule('/oauth', 'oauth', google_oauth, methods=['GET'])
bp.add_url_rule('/google', 'google', google_auth, methods=['GET'])
bp.add_url_rule('/username', 'username', add_username, methods=['GET', 'POST'])
bp.add_url_rule('/logout', 'logout', logout, methods=['GET'])
