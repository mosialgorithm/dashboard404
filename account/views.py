import random
from datetime import datetime, timedelta
from app import db
from flask import render_template, redirect, url_for, request, jsonify, session
from flask_login import login_user, current_user, logout_user
from . import account
from .forms import RegisterForm
from .models import UserModel, UserPhoneModel, UserLogModel




@account.route('/register', methods=['GET', 'POST'])
def register(): 
    if request.method == 'POST':
        # form = RegisterForm(request.form)
        full_name = request.form.get('full_name')
        phone = request.form.get('phone')
        password = request.form.get('password')
        password_confirm = request.form.get('password_confirm')
        # 
        old_user = UserModel.query.filter_by(phone=phone).first()
        if old_user:
            print('phone number is used for another user')
            return jsonify({
                'status': 'error',
                'message' : 'phone number is used for another user',
            })
        # if len(phone) != 11:
        #     print(len(phone))
        #     print('phone number is not 11 char')
        #     return jsonify({
        #         'status': 'error',
        #         'message' : 'phone number is not 11 char',
        #     })      
        if password != password_confirm:
            print('pass & pass_conf is not equal')
            return jsonify({
                'status': 'error',
                'message' : 'password and confirm_password is not equal',
            })
            
        user = UserModel()
        user.full_name = full_name
        user.phone = phone
        user.set_password(password)
        try:
            db.session.add(user)
            db.session.commit()
            print('user is addedd')
            return jsonify({
                'status': 'success',
                'message' : 'user is addedd successfully',
            })
        except Exception as ex:
            print(f'error {ex} is happened')
            return jsonify({
                'status': 'error',
                'message' : f'error {ex} is happened',
            })
            
            
    return render_template('account/register-page.html')



@account.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        phone = request.form.get('phone')
        password = request.form.get('password')
        user = UserModel.query.filter_by(phone=phone).first()
        if not user:
            return jsonify({
                'status': 'error',
                'message': 'this phone number is not registered yet',
            })
        if user.check_password(password):
            user_log = UserLogModel()
            user_log.user_id = user.id
            user_log.login_at = datetime.now()
            user_log.is_active = True
            db.session.add(user_log)
            db.session.commit()
            login_user(user)
            return jsonify({
                'status': 'success',
                'message': 'user is login successfully',
            })
        else:
            return jsonify({
                'status': 'error',
                'message': 'password is not correct',
            })
    return render_template('account/login-page.html')


@account.route('login-by-phone', methods=['GET', 'POST'])
def login_by_phone():
    if request.method == 'POST':
        phone = request.form.get('phone')
        user = UserModel.query.filter_by(phone=phone).first()
        if user is None:
            return jsonify({
                'status': 'error',
                'title': 'not_phone',
                'message': 'phone number is not register yet, please register first',
            }) 
        session['user_phone'] = phone
        random_code = random.randint(100000,999999)
        user_phone = UserPhoneModel()
        user_phone.phone = phone
        user_phone.code = random_code
        user_phone.expired_at = datetime.now() + timedelta(minutes=1)
        db.session.add(user_phone)
        db.session.commit()
        print('random_code -> ', random_code) #todo: must be send SMS instead of print
        return jsonify({
                'status': 'success',
                'message': 'code is send to phone number',
            }) 
        
    return render_template('account/login-by-phone-page.html')

@account.route('login-by-phone-auth', methods=['GET', 'POST'])
def login_by_phone_auth():
    if request.method == 'POST':
        code = request.form.get('code')
        phone = session.get('user_phone')
        if phone == None or code == None:
            return jsonify({
                    'status': 'error',
                    'message': 'data is invalid',
                }) 
            
        user_phone = UserPhoneModel.query.filter_by(phone=phone, code=code).first()
        if user_phone is None:
            return jsonify({
                    'status': 'error',
                    'message': 'data is invalid',
                }) 
        if user_phone.expired_at > datetime.now():
            user = UserModel.query.filter_by(phone=phone).first()
            login_user(user)
            return jsonify({
                'status': 'success',
                'message': 'you are loggin successfully',
            }) 
        else:
            return jsonify({
                'status': 'error',
                'message': 'timing for register code is expired',
            }) 
            
    return render_template('account/login-by-phone-auth-page.html')


@account.route('/logout')
def logout():
    current_user_id = current_user.id
    logout_user()
    user_log = UserLogModel.query.filter_by(user_id=current_user_id, is_active=True).first()
    user_log.logout_at = datetime.now()
    user_log.is_active = False
    db.session.add(user_log)
    db.session.commit()
    

    return redirect(url_for('account.login'))