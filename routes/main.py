from flask import Blueprint, render_template, request, flash, session, url_for, redirect
from extensions import current_year


main = Blueprint('main', __name__, static_folder='static', template_folder='templates')


@main.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html', current_year=current_year)