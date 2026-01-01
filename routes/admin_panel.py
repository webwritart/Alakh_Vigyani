import json
import os

from flask import Blueprint, render_template, request, flash, send_file, redirect, url_for, session, Response
from flask_login import current_user, login_required, login_user, logout_user
from extensions import current_year, db
from operations.messenger import send_email
from models.member import Role, Member, Retreat, RetreatFeedbacks, RetreatSuggestions
from operations.miscellaneous import uuid_generator


admin_panel = Blueprint('admin_panel', __name__, static_folder='static', template_folder='templates/admin_panel')


@admin_panel.route('/', methods=['GET', 'POST'])
@login_required
def main_dashboard():
    admin = db.session.query(Role).filter_by(name='admin').scalar()
    super_admin = db.session.query(Role).filter_by(name='super-admin').scalar()
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
        title = request.form.get('title')
        title_list = []
        all_retreat = db.session.query(Retreat).all()
        for retreat in all_retreat:
            title_list.append(retreat.title.lower())
        if title.lower() not in title_list:
            subtitle = request.form.get('subtitle')
            date = request.form.get('date')
            v1 = request.form.get('v1')
            v2 = request.form.get('v2')
            v3 = request.form.get('v3')
            city_country_pin = request.form.get('city_country_pin')
            landmark = request.form.get('landmark')
            a1 = request.form.get('a1')
            a2 = request.form.get('a2')
            a3 = request.form.get('a3')
            a4 = request.form.get('a4')
            a5 = request.form.get('a5')
            a6 = request.form.get('a6')
            a7 = request.form.get('a7')
            a8 = request.form.get('a8')
            a9 = request.form.get('a9')
            prerequisites = request.form.get('prerequisites')
            stuffs_to_bring = request.form.get('stuffs_to_bring')
            accommodation = request.form.get('accommodation')
            local_commutation = request.form.get('local_commutation')
            charges = request.form.get('charges')
            contact = request.form.get('contact')
            team = request.form.get('team')
            rules = request.form.get('rules')
            total_seats = request.form.get('total_seats')
            early_bird_seats = request.form.get('early_bird_seats')
            uuid = uuid_generator('Retreat')
            entry = Retreat(
                uuid=uuid,
                title=title,
                subtitle=subtitle,
                date=date,
                venue_line_1=v1,
                venue_line_2=v2,
                venue_line_3=v3,
                city_country_pin=city_country_pin,
                landmark=landmark,
                activity_1=a1,
                activity_2=a2,
                activity_3=a3,
                activity_4=a4,
                activity_5=a5,
                activity_6=a6,
                activity_7=a7,
                activity_8=a8,
                activity_9=a9,
                prerequisites=prerequisites,
                stuffs_to_bring=stuffs_to_bring,
                accommodation=accommodation,
                local_commutation=local_commutation,
                charges=charges,
                contact=contact,
                team=team,
                rules=rules,
                total_seats=total_seats,
                early_bird_seats=early_bird_seats
            )
            db.session.add(entry)
            db.session.commit()
            if request.files['cover']:
                cover = request.files['cover']
                # write compression if large and PNG to JPG conversion code here
                folder = 'static/images/retreats/'+str(uuid)+'/'
                os.makedirs(folder, exist_ok=True)
                cover_path = folder + 'cover_'+ str(uuid) +'.jpg'
                cover.save(cover_path)

            flash('Retreat details added successfully', 'success')
        else:
            flash('Retreat with same title already exists! Aborted', 'error')

    return redirect(request.referrer)

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
