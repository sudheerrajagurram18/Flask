


from flask import Flask
from flaskext.mysql import MySQL

def connection():
	
	mysql = MySQL()
	app = Flask(__name__)
	app.config['MYSQL_DATABASE_USER'] = 'admin'
	app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
	app.config['MYSQL_DATABASE_DB'] = 'employee'
	app.config['MYSQL_DATABASE_HOST'] = 'localhost'
	
	mysql.init_app(app)
	
	conn = mysql.connect()
	cursor = conn.cursor()
		
	return conn, cursor