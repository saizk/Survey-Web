from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt


db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()


def create_app(test_config=None):
    app = Flask(__name__)
    app.config["SECRET_KEY"] = b"\x8c\xa5\x04\xb3\x8f\xa1<\xef\x9bY\xca/*\xff\x12\xfb"
    
    # app.config["SQLALCHEMY_DATABASE_URI"
    # ] = "mysql+mysqldb://survey:waDBlog@localhost/Survey"
    
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Register blueprints:
    # Blueprints for auth routes
    from . import auth as auth_bp
    app.register_blueprint(auth_bp.bp)

    # Blueprints for non-auth 
    from . import main as main_bp
    app.register_blueprint(main_bp.bp)
    
    db.init_app(app)
    db.create_all(app=app)

    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        from .model import User
        # use user_id to identify the user in the table
        return User.query.get(int(user_id))

    return app