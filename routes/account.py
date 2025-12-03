from flask import Blueprint, render_template, request, flash, send_file, redirect, url_for, session
from extensions import current_year
from operations.miscellaneous import generate_captcha
from flask_login import current_user, login_required, login_user, logout_user

account = Blueprint('account', __name__, static_folder='static', template_folder='templates/account')

otp = []


@account.route('/', methods=['GET', 'POST'])
@login_required
def home():
    return render_template('account.html', current_year=current_year)


@account.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html', current_year=current_year)


@account.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html', current_year=current_year)


@account.route('/logout')
@login_required
def logout():
    return redirect(url_for('main.home'))


@account.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    return render_template('forgot_password.html', current_year=current_year)


@account.route('/set_new_password', methods=['GET', 'POST'])
def set_new_password():
    return render_template('set_new_password.html', current_year=current_year)


@account.route('/breach_report', methods=['GET', 'POST'])
def breach_report():
    return render_template('breach_report.html')