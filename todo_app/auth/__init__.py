from flask import Blueprint


auth_bp = Blueprint('auth', __name__)

from todo_app.auth import routes