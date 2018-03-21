

from flask import Flask, render_template, redirect, url_for, request
from flaskext.mysql import MySQL
from database import connection


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('login.html')
	
@app.route('/createaccount')
def createaccount():
	return render_template('createaccount.html')

@app.route('/addemp')
def addemp():
	return render_template('addemployee.html')

@app.route('/delemp')
def delemp():
	return render_template('deleteemployee.html')

@app.route('/mainpage')
def mainpage():
	return render_template('mainpage.html')
	
@app.route('/empidviewemp')
def empidviewemp():
	return render_template('empidviewemployee.html')

@app.route('/viewemp',  methods=['GET', 'POST'])
def viewemp():
	reslist = []
	conn, cursor = connection()
	if request.method == 'POST':
		emp_id = request.form['empid']		
		query = "select * from employee_info where empid='%s'" %(emp_id)
		cursor.execute(query)
		row = cursor.fetchone()
		if row is not None:
			print 'EMPLOYEE AVAILABLE TO VIEW'
			error= True
			for val in row:
				reslist.append(val)
			return render_template('viewemployee.html', error=error, reslist = reslist)
		else:
			print 'EMPLOYEE NOT AVAILABLE TO VIEW'
			error= False
			reslist.append('Employee With emp_id:'+ emp_id +' Not Available!!!')
			return render_template('viewemployee.html', error=error, reslist = reslist)

@app.route('/deleteemp',  methods=['GET', 'POST'])
def deleteemp():
	msg   = None
	error = None
	conn, cursor = connection()
	if request.method == 'POST':
		emp_id = request.form['empid']		
		query = "select * from employee_info where empid='%s'" %(emp_id)
		cursor.execute(query)
		row = cursor.fetchone()
		if row is not None:
			print 'EMPLOYEE AVAILABLE TO DELETE'
			msg = 'Employee With emp_id:'+ emp_id +' Deleted Successfully!!!'
			query = "delete from employee_info where  empid='%s'" %(emp_id)
			cursor.execute(query)
			conn.commit()
			return render_template('status.html',  message = msg)
		else:
			print 'EMPLOYEE NOT AVAILABLE TO DELETE'
			error = 'Employee With emp_id:'+ emp_id +' Not Available!!!'
			return render_template('deleteemployee.html', error = error) 
			
@app.route('/insertemp',  methods=['GET', 'POST'])
def insertemp():
	msg = None
	conn, cursor = connection()
	if request.method == 'POST':	
		msg = 'Employee Added Successfully !!'
		fn = request.form['firstname']
		ln = request.form['lastname']	
		db = request.form['dob']	
		gen = request.form['gender']	
		mn = request.form['mobilenum']	
		em = request.form['email']	
		loc = request.form['location']
		query = "INSERT INTO employee_info (fname,lname,dob,gender,mobilenum,email,location) VALUES (%s,%s,%s,%s,%s,%s,%s)"
		args = (fn, ln, db, gen, mn, em, loc)
		cursor.execute(query, args)
		conn.commit()		
		return render_template('status.html', message = msg)
	
@app.route('/validate', methods=['GET', 'POST'])
def validate():
	conn, cursor = connection()
	if request.method == 'POST':
		error = None
		un = request.form['username']
		pw = request.form['password']		
		query = "select * from admin_info where fname='%s' and password='%s'" %(un,pw)
		cursor.execute(query)
		row = cursor.fetchone()
		if row is not None:
			return render_template('mainpage.html')
		else:
			error = 'Invalid username or password. Please try again!'
			return render_template('login.html', error = error)
		
@app.route('/insertadmin', methods=['GET', 'POST'])
def login():
	conn, cursor = connection()
	if request.method == 'POST':
		fn = request.form['firstname']
		ln = request.form['lastname']		
		npw = request.form['npassword']
		cpw = request.form['cpassword']

		if npw == cpw :			
			query = "INSERT INTO admin_info (fname,lname,password) VALUES (%s,%s,%s)"
			args = (fn, ln, npw)
			cursor.execute(query, args)
			conn.commit()
			return "NPW==CPW"

if __name__ == '__main__':
	app.run(debug=True)