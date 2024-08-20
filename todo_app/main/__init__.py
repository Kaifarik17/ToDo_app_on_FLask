from flask import Blueprint


main_bp = Blueprint('main', __name__)

from todo_app.main import routes