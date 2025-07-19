import os
import datetime
import jdatetime
from pathlib import Path
import json
from app import db, app
from flask import render_template, redirect, url_for, request, jsonify, make_response
from sqlalchemy import desc
from . import admin
from flask_login import login_required
from account.models import UserModel
from .models import SiteSettingsModel
from werkzeug.utils import secure_filename





@admin.route('/')
@login_required
def index():
    return render_template('admin/dashboard.html')


@admin.route('/users')
@login_required
def users():
    all_users = UserModel.query.all()
    return render_template('admin/users/users-list-page.html', all_users=all_users)


@admin.route('/get-site-settings', methods=['GET'])
@login_required
def get_site_settings():
    settings = SiteSettingsModel.query.order_by(SiteSettingsModel.id.desc()).first()
    if settings is None:
        return jsonify({
            'status': 'empty',
            'data': [],
            'message': 'not found any data'
        })
    data = settings.__dict__
    # -------------------- convert timimg to gregorian ---------------------
    gregorian_datetime = data['start_time']
    jalali_datetime = jdatetime.datetime.fromgregorian(datetime=gregorian_datetime)
    start_time = jalali_datetime
    start_time_convert = f'{start_time.year}-{start_time.month}-{start_time.day}'
    # ------------------------------------------------------------------------
    response = jsonify({
        'title': data['title'],
        'description': data['description'],
        'email': data['email'],
        'mobile': data['mobile'],
        'phone': data['phone'],
        'address': data['address'],
        'post_code': data['post_code'],
        'start_time': start_time_convert,
        'logo': data['logo']
    })
    return make_response(response, 200)
        


@admin.route('/site-settings', methods=['GET', 'POST'])
@login_required
def site_settings():
    settings = SiteSettingsModel.query.order_by(SiteSettingsModel.id.desc()).first()
    if request.method == 'POST':
        settings = SiteSettingsModel()
        settings.title = request.form.get('title')
        settings.description = request.form.get('description')
        settings.email = request.form.get('email')
        settings.mobile = request.form.get('mobile')
        settings.phone = request.form.get('phone')
        settings.address = request.form.get('address')
        settings.post_code = request.form.get('post_code')
        # ------------ time jalali to gregorian -------------
        time = request.form.get('start_time')
        print('time is : ', time)
        year = time.split('-')[0]
        month = time.split('-')[1]
        day = time.split('-')[2]
        jalali_date = jdatetime.date(int(time.split('-')[0]), int(time.split('-')[1]), int(time.split('-')[2]))
        settings.start_time = jalali_date.togregorian()
        # ---------------------------------------------------
        if request.files:
            file = request.files.get('logo')
            if file.filename == '':
                return jsonify({
                    'status': 'error',
                    'message': 'file is not seleted'
                    })
            if file:
                directory = Path(os.path.join(app.config['UPLOAD_FOLDER'],'settings'))
                directory.mkdir(parents=True, exist_ok=True)
                location = os.path.join(directory ,secure_filename(file.filename))
                file.save(location)
                settings.logo = location
        # 
        try:
            db.session.add(settings)
            db.session.commit()
            return jsonify({
                'status': 'ok',
                'message': 'new settings is added successfully'
            })
        except Exception as ex:
            print(f'error {ex}')
            return jsonify({
                'status': 'error',
                'message': f'Error {ex} is happened, please try again'
            })
        
    return render_template('admin/settings/site-settings-page.html', settings=settings)


@admin.route('/site-image', methods=['POST'])
def site_image():
    print('site image is called')
    old_settings = SiteSettingsModel.query.filter_by(is_active=True).first()
    if request.method == 'POST':
        if request.files:
            file = request.files.get('image')
            print('file : ', file)
            if file.filename == '':
                print('No selected file') 
            if file:
                directory = Path(os.path.join(app.config['UPLOAD_FOLDER'], f'settings'))
                directory.mkdir(parents=True, exist_ok=True)
                location = os.path.join(directory ,secure_filename(file.filename))
                print(location)
                file.save(location)
                old_settings.logo = location
                db.session.commit()
                # return render_template('/admin/settings/partials/file-upload.html')
                # return redirect(url_for('admin.site_settings'))
                return jsonify({'message':'file is upload successfully'})
        else:
            # print('no file')
            return jsonify({'message':'file is not uploaded successfully, please try again'})
    return jsonify({'message': 'method is not POST !!'})
    # return redirect(url_for('admin.site_settings'))
    # return render_template('/admin/settings/partials/file-upload.html')