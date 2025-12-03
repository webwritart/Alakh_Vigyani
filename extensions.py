from flask_mail import Mail, Message
from datetime import datetime
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user


db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()

current_year = datetime.now().year