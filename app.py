import os
from flask import Flask
from dotenv import load_dotenv
from extensions import mail, db, login_manager
from routes.main import main
from routes.school import school
from routes.writings import writings
from routes.about import about
from routes.spiritual import spiritual, retreats
from routes.photography import photography
from routes.account import account
from routes.admin_panel import admin_panel
from models.member import Member, Role, Retreat, RetreatFeedbacks, RetreatSuggestions
from models.blog import Blog, Category, Tag, Comment, Reply


load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('APP_SECRET')
# app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///alakh.db"
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_URI')
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_USE_SSL'] = True
mail.init_app(app)
db.init_app(app)
login_manager.init_app(app)


app.register_blueprint(main, url_prefix='/')
app.register_blueprint(account, url_prefix='/account')
app.register_blueprint(photography, url_prefix='/photography')
app.register_blueprint(spiritual, url_prefix='/spiritual')
app.register_blueprint(school, url_prefix='/school')
app.register_blueprint(writings, url_prefix='/writings')
app.register_blueprint(about, url_prefix='/about')
app.register_blueprint(admin_panel, url_prefix='/admin_panel')

with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(member_id):
 return db.get_or_404(Member, member_id)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    # app.run(debug=True)
