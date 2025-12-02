from flask import Blueprint, render_template, request, flash, session, url_for, redirect
from extensions import current_year

spiritual = Blueprint('spiritual', __name__, static_folder='static', template_folder='templates/spiritual')



@spiritual.route('/retreats', methods=['GET', 'POST'])
def retreats():
    session['url'] = request.url
    if 'view' not in session:
        return redirect(url_for('main.coming_soon'))
    else:
        return render_template('retreats.html', current_year=current_year)