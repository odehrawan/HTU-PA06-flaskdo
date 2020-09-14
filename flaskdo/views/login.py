import sqlite3
from flask import Blueprint, render_template, request, redirect, session
from ..models.user import User
from ..db import get_db

# define our blueprint
bp = Blueprint('login', __name__)


@bp.route('/signup', methods=['GET', 'POST'])
def signup():
    # when the user requests the page over the HTTP GET
    if request.method == 'GET':
        return render_template('login/signup.html')

    # when the user submits the form over the HTTP POST
    else:
        # read values from form
        email = request.form['email']
        password = request.form['password']
        psw = request.form['psw']

        print(f"Storing {email} and {password}.")

        # get the db connection
        db = get_db()

        # insert user into db
        try:
            # execute the SQL query
            db.execute(
                "INSERT INTO User (email, password, psw) VALUES (?, ?, ?);", (email, password, psw,))

            # commit the changes to the DB
            db.commit()
            return redirect("/login")

         
        except sqlite3.Error as er:
            print('SQLite error: %s' % (' '.join(er.args)))
            return redirect("/404")


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login/login.html')
    else:
        # read login values from user
        email = request.form['email']
        password = request.form['password']

        # get db connection
        db = get_db()

        # fetch user
        try:
            # execute the SQL query
            user = db.execute(
                "SELECT * FROM User WHERE email=?;", (email,)).fetchone()

            # if the user was found
            if user and user['password'] == password:
                # store the user ID in the session
                session['uid'] = user['id']
                session['first_name'] = user['first_name']

                # redirect to index
                return redirect('/edit/profile')
            # if the user was not found
            else:
                # render the login page with an error message
                return render_template('login/login.html', message="Invalid credentials. Please try again.")
        except sqlite3.Error as er:
            print('SQLite error: %s' % (' '.join(er.args)))
            return redirect("/404")


@bp.route('/logout')
def logout():
    if session.pop('uid', None):
        return redirect('/')
