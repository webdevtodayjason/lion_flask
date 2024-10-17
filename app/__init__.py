from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_wtf import CSRFProtect
from flask_wtf.csrf import generate_csrf  # Import generate_csrf
from flask_mail import Mail

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
csrf = CSRFProtect()
mail = Mail()

def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static')
    app.config['SECRET_KEY'] = 'your_secret_key_here'  # Replace with a strong secret key
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lion_report.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Add this configuration to suppress the default login message
    app.config['LOGIN_MESSAGE'] = ''  # Suppress default login message

    app.config['MAIL_SERVER'] = 'smtp.example.com'       # Replace with your SMTP server
    app.config['MAIL_PORT'] = 587                        # Replace with your SMTP port
    app.config['MAIL_USE_TLS'] = True                    # True if using TLS
    app.config['MAIL_USERNAME'] = 'your_email@example.com'  # Replace with your email
    app.config['MAIL_PASSWORD'] = 'your_email_password'  # Replace with your email password

    mail.init_app(app)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'
    csrf.init_app(app)
    Bootstrap(app)

    @app.context_processor
    def inject_csrf_token():
        return dict(csrf_token=generate_csrf())

    with app.app_context():
        from . import routes
        app.register_blueprint(routes.main)
        # db.create_all()

    return app
