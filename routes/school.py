from flask import Blueprint, render_template, request, flash, session, url_for, redirect
from extensions import current_year


school = Blueprint('school', __name__, static_folder='static', template_folder='templates/school')


@school.route('/school', methods=['GET', 'POST'])
def home():
    return render_template('school.html', current_year=current_year)
