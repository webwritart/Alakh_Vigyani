from datetime import date
from flask import Blueprint, render_template, request, flash, send_file, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import current_year, db
from models.member import Member, Role
from operations.miscellaneous import generate_captcha, calculate_age
from operations.messenger import send_email
from flask_login import current_user, login_required, login_user, logout_user
import random


account = Blueprint('account', __name__, static_folder='static', template_folder='templates/account')

otp = []
today_date = date.today()


@account.route('/', methods=['GET', 'POST'])
@login_required
def home():
    return render_template('account.html', current_year=current_year)


@account.route('/register', methods=['GET', 'POST'])
def register():
    num_list = []
    uuid_list = []

    result = db.session.query(Member).all()
    for user in result:
        uuid_list.append(user.uuid)
        num = user.phone
        if len(num) == 10:
            user_no = f"91{num}"
        elif len(num) == 11 and num[0] == '0':
            user_no = f'91{num[1:]}'
        elif len(num) == 12 and num[:2] == '91':
            user_no = num
        elif len(num) == 13:
            user_no = num[3:]
        else:
            user_no = num
        num_list.append(user_no)

    if request.method == 'POST':
        if request.form.get('submit') == 'register':
            ph = request.form.get('phone')
            if len(ph) == 10:
                phone = f"91{ph}"
            elif len(ph) == 11 and ph[0] == '0':
                phone = f'91{ph[1:]}'
            elif len(ph) == 12 and ph[:2] == '91':
                phone = ph
            elif len(ph) == 13:
                phone = ph[3:]
            else:
                phone = ph

            email = request.form.get('email')
            state = request.form.get('state')
            result = db.session.execute(db.select(Member).where(Member.email == email))
            user = result.scalar()
            if user:
                flash("You've already signed up with that email, log in instead!", "error")
                return redirect(url_for('account.login'))
            if phone in num_list:
                flash(
                    "Already an account exists with phone number. Please register with different phone number or log in",
                    "error")
                return redirect(url_for('account.register'))
            hash_and_salted_password = generate_password_hash(
                request.form.get('password'),
                method='pbkdf2:sha256',
                salt_length=8
            )
            # date_ = request.form.get('date')
            # if len(date_) < 2:
            #     date_ = "0" + date_
            # month = request.form.get('month')
            # if len(month) < 2:
            #     month = "0" + month
            # year = request.form.get('year')
            # dob = f"{year}-{month}-{date_}"
            dob = request.form.get('dob')
            age = calculate_age(dob)

            unique = False
            uuid = ''
            while not unique:
                u = random.randint(100000, 999999)
                if u not in uuid_list:
                    uuid = u
                    unique = True



            new_user = Member(
                email=request.form.get('email'),
                password=hash_and_salted_password,
                name=request.form.get('name'),
                phone=request.form.get('phone'),
                whatsapp=request.form.get('whatsapp'),
                profession=request.form.get('profession'),
                sex=request.form.get('sex'),
                dob=dob,
                state=state,
                registration_date=today_date,
                uuid=uuid
            )
            db.session.add(new_user)
            db.session.commit()

            all_users = db.session.query(Member)
            super_admin = db.session.query(Role).filter_by(name='super-admin').scalar()

            if len(all_users.all()) == 1:
                all_users[0].role.append(super_admin)
                db.session.commit()

            login_user(new_user)
            session['logged_in'] = True

            mail = render_template('mails/registration_success.html')
            send_email('Registration success!', [email],
                               '',
                               mail, '')
            mail_message = f'New Registration:\n\nName: {request.form.get("name")}\nEmail: {request.form.get("email")}\n' \
                           f'Phone: {request.form.get("phone")}' \
                           f'Sex: {request.form.get("sex")}\nProfession: {request.form.get("profession")}\n' \
                           f'State: {request.form.get("state")}\n\n'
            send_email('New Registration!', ['shwetabhartist@gmail.com'], mail_message, '', '')
            if 'url' in session:
                return redirect(session['url'])
            return redirect(url_for('account.home', name=current_user.name.split()[0]))
    return render_template("register.html", logged_in=current_user.is_authenticated, current_year=current_year)


@account.route('/login', methods=['GET', 'POST'])
def login():
    num_list = []
    raw_num_list = []
    result = db.session.query(Member)
    for user in result:
        num = user.phone
        raw_num_list.append(num)
        if len(num) == 10:
            user_no = f"91{num}"
        elif len(num) == 11 and num[0] == '0' or '+':
            user_no = f'91{num[1:]}'
        elif len(num) == 12 and num[:2] == '91':
            user_no = num
        elif len(num) == 13 and num[:3] == '+91':
            user_no = num[3:]
        else:
            user_no = num
        num_list.append(user_no)
    if request.method == 'POST':
        if request.form.get('password2'):
            pwd = request.form.get('password2')
            retype_pwd = request.form.get('retype-password2')
            if pwd != retype_pwd:
                flash("Retyped password did not match! Please try again.", "error")
                return render_template('update_account.html')
            hash_and_salted_password = generate_password_hash(
                pwd,
                method='pbkdf2:sha256',
                salt_length=8
            )
            current_user.password = hash_and_salted_password
            current_user.sex = request.form.get('sex')
            date_ = request.form.get('date')
            if len(date_) < 2:
                date_ = "0" + date_
            month = request.form.get('month')
            if len(month) < 2:
                month = "0" + month
            year = request.form.get('year')
            current_user.dob = f"{year}-{month}-{date_}"
            current_user.profession = request.form.get('profession')
            current_user.state = request.form.get('state')
            db.session.commit()
            return redirect(url_for('account.home'))
        data = request.form.get('email-phone')
        if '@' in data:
            email = data
            result = db.session.execute(db.select(Member).where(Member.email == email))
            user = result.scalar()
        else:
            user_phone = ''
            ph = data
            if len(ph) == 10:
                phone = f"91{ph}"
            elif len(ph) == 11 and ph[0] == '0' or '+':
                phone = f'91{ph[1:]}'
            elif len(ph) == 12 and ph[:2] == '91':
                phone = ph
            elif len(ph) == 13 and ph[:3] == '+91':
                phone = ph[3:]
            else:
                phone = ph
            if phone in num_list:
                index = num_list.index(phone)
                user_phone = raw_num_list[index]
            result = db.session.execute(db.select(Member).where(Member.phone == user_phone))
            user = result.scalar()
        password = request.form.get('password')

        # Email or Phone doesn't exist or password incorrect:
        if not user:
            flash("That Email or Phone does not exist, please try again.", category="error")
        elif not check_password_hash(user.password, password):
            flash('Password incorrect, please try again.', category='error')
        else:
            login_user(user)
            session['logged_in'] = True
            if 'url' in session:
                return redirect(session['url'])
            if db.session.query(Role).filter(Role.name == 'admin').scalar() in current_user.role:
                return redirect(url_for('manager.home'))
            if db.session.query(Role).filter(Role.name == 'animation_admin').scalar() in current_user.role:
                return redirect(url_for('animation_admin.home'))
            if db.session.query(Role).filter(Role.name == 'client').scalar() in current_user.role:
                return redirect(url_for('client_section.client_dashboard'))
            if not current_user.sex or current_user.sex == '':
                return render_template('update_account.html')
            if request.form.get('prev-page') == 'enroll':
                flash("You are successfully logged in. Now proceed to enroll", "success")
                return redirect(url_for('payment.home'))
            if request.form.get('prev-page') == 'change-password':
                flash("You are successfully logged in. Now proceed to change password", "success")
                return redirect(url_for('account.change_password'))
            return redirect(url_for('account.home', name=current_user.name.split()[0]))
    return render_template('login.html', current_year=current_year)


@account.route('/logout')
@login_required
def logout():
    logout_user()
    session['logged_in'] = False
    if 'url' in session:
        return redirect(session['url'])
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