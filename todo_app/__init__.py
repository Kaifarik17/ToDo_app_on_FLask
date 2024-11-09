from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

from config import Config


db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message ="Please login to access this page"
csrf = CSRFProtect()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)

    from todo_app.main import main_bp
    app.register_blueprint(main_bp)

    from todo_app.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from todo_app.errors import errors_bp
    app.register_blueprint(errors_bp)


    return app

from todo_app import models