import os

# 是否开启debug模式
DEBUG = True
SERVER_SECRET = 'a3c9f9b10a2e4a8fb0931fc2ed5ab1d4f3c5c34c79a6e6d0'

# 读取数据库环境变量
username = os.environ.get("MYSQL_USERNAME", 'root')
password = os.environ.get("MYSQL_PASSWORD", 'KXh9VsgZ')
db_address = os.environ.get("MYSQL_ADDRESS", 'sh-cynosdbmysql-grp-c25eh650.sql.tencentcdb.com:29998')
