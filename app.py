import jinja_partials
from flask import Flask, render_template, redirect, flash, url_for, jsonify, g
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from config import Development




app = Flask(__name__)

ma = Marshmallow(app)

jinja_partials.register_extensions(app)

app.config.from_object(Development)

# ----------------------------- CONFIGS_OF_LOGIN_MANAGER -----------------------
login = LoginManager()
login.login_view = 'login'
login.login_message_category = 'info'
login.init_app(app)
# ------------------------------------------------------------------------------

db = SQLAlchemy(app)

# migrate = Migrate(app, db, compare_type=True)
migrate = Migrate(app, db)




@app.route("/")
def index():
    # return render_template('base.html')
    return jsonify({
        'status': 200,
        'programmer': 'mosi',
        'message': 'Flask Dashboard by Alpine & HTMX',
        'data': []
    })

@app.route('/result')
def result():
    return "hello world"



# -------------------------------- Blueprint Configs ------------------------
from account import account
from admin import admin


app.register_blueprint(account)
app.register_blueprint(admin)



# ....................... login user handler ................................
from account.models import UserModel

@login.user_loader
def userLoader(user_id):
    return UserModel.query.get(user_id)

@login.unauthorized_handler
def unauthorized():
    flash('You must login first', 'warning')
    return redirect(url_for('account.login'))
# ...........................................................................



# from admin.models import SiteSettingsModel
# g.site_settings = SiteSettingsModel.query.order_by(SiteSettingsModel.id.desc()).first()



if __name__ == "__main__":
    app.run()