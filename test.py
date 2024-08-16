# from flask import Flask
# from flask_mysqldb import MySQL

# app = Flask(__name__)

# Configure MySQL

# app.config['MYSQL_HOST'] = "sh-cynosdbmysql-grp-c25eh650.sql.tencentcdb.com"
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:890527@localhost/venue_booking'
# app.config['MYSQL_HOST'] = "localhost"
# app.config['MYSQL_USER'] = "root"
# # app.config['MYSQL_PASSWORD'] = "KXh9VsgZ"
# app.config['MYSQL_PASSWORD'] = "890527"
# app.config['MYSQL_DB'] = 'venue_booking'
# # app.config['MYSQL_PORT'] = 29998
# app.config['MYSQL_PORT'] = 3306

#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:890527@localhost/venue_booking'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            login_user(user)
            return redirect(url_for('admin.index'))
    return '''
    <form method="POST">
        Username: <input type="text" name="username"><br>
        Password: <input type="password" name="password"><br>
        <input type="submit" value="Login">
    </form>
    '''

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

class MyModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login'))

admin = Admin(app, name='MyApp', template_mode='bootstrap3')
admin.add_view(MyModelView(User, db.session))

if __name__ == '__main__':
    app.run()
