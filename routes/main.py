from flask import Blueprint, render_template, request, flash, session, url_for, redirect
from extensions import current_year, db
from operations.miscellaneous import generate_captcha
from models.member import Role
from flask_login import current_user

main = Blueprint('main', __name__, static_folder='static', template_folder='templates/main')


@main.route('/coming_soon', methods=['GET', 'POST'])
def coming_soon():
    return render_template('coming_soon.html', current_year=current_year)


@main.route('/', methods=['GET', 'POST'])
def home():
    session['url'] = request.url
    if 'view' not in session:
        return render_template('coming_soon.html', current_year=current_year)
    else:
        # super_admin = db.session.query(Role).filter_by(name='super-admin').scalar()
        # print(super_admin)
        # current_user.role.append(super_admin)
        # db.session.commit()
        return render_template('index.html', logged_in=current_user.is_authenticated, current_year=current_year)

@main.route('/team_login', methods=['GET', 'POST'])
def team_login():
    password = 'b00800m'
    captcha_value, captcha_uri = generate_captcha()
    session['captcha_value'] = captcha_value
    session['pwd'] = password
    return render_template('view_login.html', captcha=captcha_uri, current_year=current_year)


@main.route('/captcha_verification', methods=['GET', 'POST'])
def captcha_verification():
    if request.method == 'POST':
        captcha_value = session.get('captcha_value')
        if request.form.get('captcha') != captcha_value:
            flash("Wrong Captcha!", "error")
            return redirect(url_for('main.team_login'))
        else:
            # name = request.form.get('name')
            # email = request.form.get('email')
            # email2 = request.form.get('email2')
            # msg = request.form.get('message')
            # if email == email2:
            #     message = f'{msg}\n\n\nSENDER DETAILS:\nName: {name}\nEmail: {email}\n'
            #
            #     success_msg = (f'Dear {name},\n\nThanks for sending me a message.\nI will get back to you as soon as possible. '
            #                f':)\n\n\nShwetabh Suman\nConcept Artist & Illustrator\nNew Delhi, India')
            #     send_email('IMPORTANT!! - Main Portfolio', ['shwetabhartist@gmail.com'], email, message, '', '')
            #     send_email('MESSAGE SENT - Shwetabh Suman', [email], 'shwetabhartist@gmail.com', success_msg, '', '')
            #     flash('Message sent successfully!', 'success')
            # else:
            #     flash("The email doesn't match!", "error")
    # check entered password and allow view--------------------------------------------------------------------
            password = session['pwd']
            if request.form.get('pwd') == password:
                session['view'] = 'allow'
                print('pwd matched and view added to session')
                return redirect(session.get('url'))
            else:
                flash("Wrong Password!", "error")
                return redirect(url_for('main.team_login'))
    return redirect(session.get('url'))


@main.route('/privacy_policy')
def privacy_policy():
    return render_template('privacy_policy.html', logged_in=current_user.is_authenticated, current_year=current_year)