from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from flask_mysqldb import MySQL

import pymysql
import config

# 因MySQLDB不支持Python3，使用pymysql扩展库代替MySQLDB库
pymysql.install_as_MySQLdb()

# 初始化web应用
app = Flask(__name__, instance_relative_config=True)
app.config['DEBUG'] = config.DEBUG
app.secret_key = config.SERVER_SECRET

# 设定数据库链接
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://{}:{}@{}/venue_booking'.format(config.username, config.password,
                                                                             config.db_address)

# app.config['MYSQL_HOST'] = "sh-cynosdbmysql-grp-c25eh650.sql.tencentcdb.com"
# app.config['MYSQL_USER'] = "root"
# app.config['MYSQL_PASSWORD'] = "KXh9VsgZ"
# app.config['MYSQL_DB'] = 'venue_booking'
# app.config['MYSQL_PORT'] = 29998

# mysql = MySQL(app)

# 初始化DB操作对象
db = SQLAlchemy(app)

# 加载控制器
from wxcloudrun import views

# 加载配置
app.config.from_object('config')


