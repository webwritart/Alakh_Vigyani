from flask import Blueprint, render_template, request, flash, session, url_for, redirect
from extensions import current_year


writings = Blueprint('writings', __name__, static_folder='static', template_folder='templates/writings')


@writings.route('/writings', methods=['GET', 'POST'])
def home():
    return render_template('writings.html', current_year=current_year)
