from flask import render_template, redirect, url_for
from . import admin
from flask_login import login_required
from account.models import UserModel


@admin.route('/')
@login_required
def index():
    return render_template('admin/dashboard.html')


@admin.route('/users')
@login_required
def users():
    all_users = UserModel.query.all()
    return render_template('admin/users/users-list-page.html', all_users=all_users)