import os
import jdatetime
from pathlib import Path
from app import db, app
from flask import render_template, redirect, url_for, request, jsonify, make_response
from sqlalchemy import desc
from . import admin
from flask_login import login_required
from account.models import UserModel
from .models import SiteSettingsModel
from werkzeug.utils import secure_filename
from .schemas import user_schema, users_schema





@admin.route('/')
@login_required
def index():
    return render_template('admin/dashboard.html')


@admin.route('/user-json/<int:user_id>')
@login_required
def user_json(user_id):
    user = UserModel.query.get_or_404(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404
    result =  user_schema.dump(user)
    return jsonify(result)


@admin.route('/user/<int:user_id>')
@login_required
def user(user_id):
    user = UserModel.query.get_or_404(user_id)
    
    return render_template('admin/users/user-single-page.html', user=user)


@admin.route('/users-json')
@login_required
def users_json():
    # all_users = UserModel.query.all()
    # page = request.args.get('page', 1, type=int)
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 4, type=int)
    per_page = 4
    pagination = UserModel.query.order_by(UserModel.id.desc()).paginate(page=page, per_page=per_page, error_out=False)
    result =  users_schema.dump(pagination)
    return jsonify({
        'data': result,
        'pagination': {
            'current_page': pagination.page,
            'total_pages': pagination.pages,
            'total_items': pagination.total,
            'per_page': pagination.per_page,
            'has_next': pagination.has_next,
            'has_prev': pagination.has_prev,
            # 'next_page_url': f'/items?page={pagination.next_num}&per_page={per_page}' if pagination.has_next else None,
            # 'prev_page_url': f'/items?page={pagination.prev_num}&per_page={per_page}' if pagination.has_prev else None,
        }
    })


@admin.route('/users')
@login_required
def users():
    # print('users path is clicked')
    # page = request.args.get('page', 1, type=int)
    # per_page = 4
    # all_users = UserModel.query.order_by(UserModel.id.desc()).paginate(page=page, per_page=per_page, error_out=False)
    # for user in all_users:
    #     print(user)
    # print('*'*30)
    # all_users = UserModel.query.all()
    # result =  users_schema.dump(all_users)
    return render_template('admin/users/users-list-page.html')


@admin.route('/user-add', methods=['POST'])
@login_required
def user_add():
    # user_data = request.get_json()
    user_phone = request.form.get('phone')
    old_user = UserModel.query.filter_by(phone=user_phone).first()
    if old_user:
        return jsonify({
            'status': 'error',
            'message': 'An user is register by this phone number previously'
        })
    new_user = UserModel()
    new_user.full_name = request.form.get('full_name')
    new_user.phone = user_phone
    new_user.set_password(request.form.get('full_name'))
    try:
        new_user.save()
        return jsonify({
            'status': 'success',
            'message': f'user by {user_phone} is registered, successfully'
        })
    except Exception as ex:
        return jsonify({
            'status': 'error',
            'message': f'error {ex} is happened'
        })



@admin.route('/user-delete/<int:user_id>', methods=['DELETE'])
@login_required
def user_delete(user_id):
    print('user delete id called')
    user = UserModel.query.get_or_404(user_id)
    full_name = user.full_name
    print('full name is : ', full_name)
    try:
        user.remove()
        print('user is deleted !!!!!!!!!1')
        return jsonify({
        'status': 'ok',
        'user': full_name
    })
    except Exception as ex:
        return jsonify({
            "status": "error",
            "message": f"error {ex} is happened !!, please try again"
        })
    


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