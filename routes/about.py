from flask import Blueprint, render_template, request, flash, session, url_for, redirect
from extensions import current_year, db
from flask_login import current_user
from models.member import Role


about = Blueprint('about', __name__, static_folder='static', template_folder='templates/about')


@about.route('/about', methods=['GET', 'POST'])
def home():
    session['url'] = request.url
    if 'view' not in session:
        return redirect(url_for('main.coming_soon'))
    else:
        super_admin = db.session.query(Role).filter_by(name='super-admin').scalar()
        admin = db.session.query(Role).filter_by(name='admin').scalar()
        return render_template('about.html', logged_in=current_user.is_authenticated,current_year=current_year,
                               super_admin=super_admin, admin=admin)
