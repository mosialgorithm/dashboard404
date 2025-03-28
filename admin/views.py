from flask import render_template, redirect, url_for
from . import admin
from flask_login import login_required


@admin.route('/')
@login_required
def index():
    return render_template('admin/index.html')
