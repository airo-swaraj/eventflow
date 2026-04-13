from flask import Flask
from flask_mysqldb import MySQL
from flask_mail import Mail
from flask_bcrypt import Bcrypt
from .config import Config

mysql = MySQL()
mail = Mail()
bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    mysql.init_app(app)
    mail.init_app(app)
    bcrypt.init_app(app)

    from .routes.auth import auth_bp
    from .routes.dashboard import dashboard_bp
    from .routes.events import events_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(events_bp)

    return app