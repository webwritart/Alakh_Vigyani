import os

from flask import Flask
from dotenv import load_dotenv
from extensions import mail
from routes.main import main
from routes.school import school
from routes.writings import writings
from routes.about import about
from routes.spiritual import spiritual


load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('APP_SECRET')
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_USE_SSL'] = True
mail.init_app(app)


app.register_blueprint(main, url_prefix='/')
app.register_blueprint(spiritual, url_prefix='/spiritual')
app.register_blueprint(school, url_prefix='/school')
app.register_blueprint(writings, url_prefix='/writings')
app.register_blueprint(about, url_prefix='/about')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    # app.run(debug=True)
