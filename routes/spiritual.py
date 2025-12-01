from flask import Blueprint, render_template, request, flash, session, url_for, redirect
from extensions import current_year

spiritual = Blueprint('spiritual', __name__, static_folder='static', template_folder='templates/spiritual')

@spiritual.route('/retreats', methods=['GET', 'POST'])
def retreats():
    return render_template('retreats.html', current_year=current_year)