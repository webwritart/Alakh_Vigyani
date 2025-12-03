from flask import Blueprint, render_template, request, flash, session, url_for, redirect
from sqlalchemy.sql.functions import current_user
from flask_login import current_user
from extensions import current_year

photography = Blueprint('photography', __name__, static_folder='static', template_folder='templates/photography')



@photography.route('/', methods=['GET', 'POST'])
def home():
    session['url'] = request.url
    if 'view' not in session:
        return redirect(url_for('main.coming_soon'))
    else:
        return render_template('photography.html', logged_in=current_user.is_authenticated, current_year=current_year)