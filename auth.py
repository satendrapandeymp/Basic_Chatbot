from flask import Flask, render_template, request,  redirect, session, flash
from functools import wraps
from passlib.hash import sha256_crypt
from MySQLdb import escape_string as thwart
import MySQLdb, time

conn = MySQLdb.connect("localhost","pandey","  ","flask")
c = conn.cursor()

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            return redirect('/login')
    return wrap

def register():
	error = None
	if request.method == 'POST':
		username = thwart(request.form['username'])
		password = request.form['password']
		email = thwart(request.form['email'])
		check = c.execute("SELECT * from auth_chatbot WHERE username = '{0}'".format(username))
		if int(check)>0:
		    flash("That username is already taken, please choose another")
		    return render_template('register.html')
		else:
		    password = sha256_crypt.encrypt(password)
		    c.execute("INSERT INTO auth_chatbot (time, username, password, is_active, email) VALUES ('{0}','{1}','{2}','{3}','{4}')".format(time.time(), username, password, 0, 0, email))
		    conn.commit()
		    session['logged_in'] = True
		    session['user'] = username
		    flash('You were just logged in')
		    return redirect('/')
        return render_template('register.html', error=error)

def login():
	error = None
	if request.method == 'POST':
		username = thwart(request.form['username'])
		password = request.form['password']
		data = c.execute("SELECT * from auth_chatbot WHERE username = '{0}'".format(username))
		if int(data)>0:
		    data = c.fetchone()[2]
		    if sha256_crypt.verify(password, data):
				session['logged_in'] = True
				session['user'] = username
				return redirect('/')
		    else:
			    error = 'Wrong username and password'
		else:
		    error = 'Wrong username and password'
	return render_template('login.html', error=error)

def logout():
    session.pop('logged_in', None)
    flash('You were just logged out')
    return redirect('/login')
