from flask import Flask, render_template, redirect, flash, url_for, jsonify
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Development
from flask_moment import Moment



app = Flask(__name__)

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

moment = Moment(app)




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




if __name__ == "__main__":
    app.run()