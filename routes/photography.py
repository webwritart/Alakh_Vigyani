from flask import Blueprint, render_template, request, flash, session, url_for, redirect
from extensions import current_year

photography = Blueprint('photography', __name__, static_folder='static', template_folder='templates/photography')



@photography.route('/', methods=['GET', 'POST'])
def home():
    session['url'] = request.url
    if 'view' not in session:
        return redirect(url_for('main.coming_soon'))
    else:
        return render_template('photography.html', current_year=current_year)