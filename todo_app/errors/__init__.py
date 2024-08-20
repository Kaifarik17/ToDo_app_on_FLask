from flask import Blueprint


errors_bp = Blueprint('errors', __name__)

from todo_app.errors import routes