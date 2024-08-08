import os

# 是否开启debug模式
DEBUG = True
SERVER_SECRET = 'a3c9f9b10a2e4a8fb0931fc2ed5ab1d4f3c5c34c79a6e6d0'
APP_ID = 'wx666e0c0e26d4d33e'
APP_SECRET = '9c351869c1c6e30160dc832796dfdacc'

# 读取数据库环境变量
username = os.environ.get("MYSQL_USERNAME", 'root')
password = os.environ.get("MYSQL_PASSWORD", 'KXh9VsgZ')
db_address = os.environ.get("MYSQL_ADDRESS", 'sh-cynosdbmysql-grp-c25eh650.sql.tencentcdb.com:29998')
