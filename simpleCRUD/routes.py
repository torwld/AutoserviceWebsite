from sqlalchemy import exc

from simpleCRUD import db, app
from flask import render_template, redirect, url_for, request, flash
from simpleCRUD.db_models import Users, Cars, RepairRequests, Repairtypes
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, current_user, logout_user
import re


@app.route('/')
def home():
    return render_template('login.html')


@app.route('/login', methods=['GET', 'POST'])
def log_user():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if email and password:
            user = Users.query.filter_by(email=email).first()

            if user and check_password_hash(user.password, password):
                if user.role == 1:
                    login_user(user)
                    return redirect(url_for('userpage'))
                if user.role == 2:
                    login_user(user)
                    return redirect(url_for('managerpage'))
            else:
                flash("Неверный email или пароль")
        else:
            flash("Введите пароль и email")
    return render_template('login.html')


@app.route("/reg", methods=['GET', 'POST'])
def reg():
    if request.method == 'POST':
        login = request.form.get('log')
        user_email = request.form.get('email')
        password = request.form.get('psw')
        password_again = request.form.get('psw_repeat')

        mass = request.form.to_dict()
        print(mass)
        if not (user_email or password_again or password):
            flash('Пожалуйста, заполните все поля')
        elif not check_email(user_email):
            flash("Email некорректен")
        elif len(password) < 6:
            flash("Слишком слабый пароль. Пароль должен содержать не менее 6 символов")
        elif password != password_again:
            flash("Пароли не совпадают")
        elif Users.query.filter_by(email=user_email).first() or Users.query.filter_by(login=login).first():
            flash('Аккаунт с данным email или логином уже зарегистрирован')
        else:
            new_user = Users(
                login=login,
                email=user_email,
                password=generate_password_hash(password)
            )
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('log_user'))
    return render_template('reg_page.html')


@app.route('/userpage')
@login_required
def userpage():
    cars = Cars.query.filter_by(owner_id=current_user.id).all()
    user_repair_requests = db.session.query(RepairRequests, Repairtypes, Cars).\
        outerjoin(Repairtypes, RepairRequests.repair_type == Repairtypes.id).\
        outerjoin(Cars, RepairRequests.client_car == Cars.car_id).filter_by(owner_id = current_user.id).all()

    repair_works = Repairtypes.query.all()
    return render_template('userspage.html', username=current_user.login, cars=cars, user_repair_requests = user_repair_requests, repair_works = repair_works)


@app.route('/carpage')
@login_required
def add_car_page():
    return render_template('cars.html')


@app.route('/addcar', methods=['POST'])
@login_required
def add_car():
    if request.method == 'POST':
        vin_num = request.form['VIN']
        car_mark = request.form['mark']
        car_model = request.form['model']
        year = request.form['year']
        mass2 = request.form.to_dict()
        print(mass2)

        new_car = Cars(
            vin_number=vin_num,
            mark=car_mark,
            model=car_model,
            prod_year=year,
            owner_id=current_user.id)

        db.session.add(new_car)
        db.session.commit()

        return redirect(url_for('userpage'))
    return render_template('cars.html')


@app.route('/delete_car/<int:car_id>')  # troubles with making it through post
@login_required
def delete_car(car_id):
    Cars.query.filter_by(car_id=car_id).delete()
    db.session.commit()
    return redirect(url_for('userpage'))


@app.route('/add_repair_request', methods=['POST'])
@login_required
def add_repair_request():
    if request.method == 'POST':
        work_type = Repairtypes.query.filter_by(description=request.form.get('type')).first()
        text_info = request.form.get('descr')
        car = Cars.query.filter_by(vin_number=request.form['vin_number']).first()
        date_req = request.form.get('date')
        time_req = request.form.get('time')

        mass2 = request.form.to_dict()
        print(mass2)
        print(car, "машина")

        new_request = RepairRequests(
            description = text_info,
            repair_type = work_type.id,
            client_id = current_user.id,
            client_car = car.car_id,
            date = date_req,
            time = time_req
        )

        db.session.add(new_request)
        db.session.commit()

    return redirect(url_for('userpage'))

#@app.route('/update_repair_request', methods = ['POST'])
#@login_required
#def update_request():
    #pass

@app.route('/delete_repair_request/<int:req_id>')
@login_required
def delete_repair_request(req_id):
    RepairRequests.query.filter_by(req_id = req_id).delete()
    db.session.commit()
    return redirect(url_for('userpage'))

@app.route('/managerpage', methods=['GET', 'POST'])
@login_required
def managerpage():
    current_manager_name = current_user.login
    repair_request_info = db.session.query(RepairRequests, Users, Cars, Repairtypes). \
        outerjoin(Users, RepairRequests.client_id == Users.id). \
        outerjoin(Cars, RepairRequests.client_car == Cars.car_id). \
        outerjoin(Repairtypes, RepairRequests.repair_type == Repairtypes.id).all()
    print(repair_request_info)

    return render_template('managerpage.html', repair_request_info=repair_request_info,
                           current_manager_name=current_manager_name)


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('log_user'))


def check_email(check_email):
    result = re.search(r'@\w+\W\w+', check_email)
    return result


