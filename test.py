from flask import Flask
from flask_mysqldb import MySQL

app = Flask(__name__)

# Configure MySQL

# app.config['MYSQL_HOST'] = "sh-cynosdbmysql-grp-c25eh650.sql.tencentcdb.com"
# app.config['MYSQL_HOST'] = "localhost"
# app.config['MYSQL_USER'] = "root"
# # app.config['MYSQL_PASSWORD'] = "KXh9VsgZ"
# app.config['MYSQL_PASSWORD'] = "890527"
# app.config['MYSQL_DB'] = 'venue_booking'
# # app.config['MYSQL_PORT'] = 29998
# app.config['MYSQL_PORT'] = 3306



class Config:
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = '890527'
    MYSQL_DB = 'venue_booking'
    MYSQL_HOST = 'localhost'
    MYSQL_PORT = 3306
    MYSQL_CURSORCLASS = 'DictCursor'
    SQLALCHEMY_DATABASE_URI = 'mysql://root:890527@localhost/venue_booking'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    APP_ID = 'wx666e0c0e26d4d33e'
    APP_SECRET = '9c351869c1c6e30160dc832796dfdacc'
    SERVER_SECRET = 'a3c9f9b10a2e4a8fb0931fc2ed5ab1d4f3c5c34c79a6e6d0'

app.config.from_object(Config)
mysql = MySQL(app)

@app.route('/')
def index():
    # Use the MySQL connection
    
    
    


    try:
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM venues')
        row = cur.fetchone()
        cur.close()

        return str(row)
    except Exception as e:
        return f"An error occurred: {e}"

if __name__ == '__main__':
    app.run(debug=True)