from flask import Blueprint, render_template, request, flash, send_file, redirect, url_for, session
from flask_login import current_user, login_required, login_user, logout_user
from extensions import current_year, db
from operations.messenger import send_email


admin_panel = Blueprint('admin_panel', __name__, static_folder='static', template_folder='templates/admin_panel')


@admin_panel.route('/', methods=['GET', 'POST'])
@login_required
def main_dashboard():
    return render_template('main_dashboard.html', current_year=current_year)