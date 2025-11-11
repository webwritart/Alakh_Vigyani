from flask_mail import Mail, Message
from datetime import datetime


mail = Mail()
current_year = datetime.now().year