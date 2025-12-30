from flask import Blueprint, render_template, request, flash, send_file, redirect, url_for, session, Response
from flask_login import current_user, login_required, login_user, logout_user
from extensions import current_year, db
from operations.messenger import send_email
from models.member import Role, Member, Retreat, RetreatFeedbacks, RetreatSuggestions


admin_panel = Blueprint('admin_panel', __name__, static_folder='static', template_folder='templates/admin_panel')


@admin_panel.route('/', methods=['GET', 'POST'])
@login_required
def main_dashboard():
    admin = db.session.query(Role).filter_by(name='admin').scalar()
    super_admin = db.session.query(Role).filter_by(name='super-admin').scalar()
    print(admin)
    print(super_admin)
    return render_template('main_dashboard.html', current_year=current_year)


@admin_panel.route('/homepage', methods=['GET', 'POST'])
@login_required
def homepage():
    return render_template('admin_homepage.html', current_year=current_year)


@admin_panel.route('/retreats', methods=['GET', 'POST'])
@login_required
def retreats():
    return render_template('admin_retreats.html', current_year=current_year)


@admin_panel.route('/submit_new_retreat', methods=['GET', 'POST'])
def submit_new_retreat():
    if request.method == 'POST':
        data = request.get_json()
        print(data)
    return Response(status=204)

@admin_panel.route('/school', methods=['GET', 'POST'])
@login_required
def school():
    return render_template('admin_school.html', current_year=current_year)


@admin_panel.route('/photography', methods=['GET', 'POST'])
@login_required
def photography():
    return render_template('admin_photography.html', current_year=current_year)


@admin_panel.route('/blog', methods=['GET', 'POST'])
@login_required
def blog():
    return render_template('admin_blog.html', current_year=current_year)


@admin_panel.route('/new_retreat', methods=['GET', 'POST'])
def new_retreat_datafeed():
    pass