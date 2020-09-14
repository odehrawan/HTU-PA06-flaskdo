import sqlite3
from flask import Blueprint, render_template, request, redirect, session, url_for
from ..models.user import User
from ..db import get_db


# define our blueprint
bp = Blueprint('profile', __name__)


@bp.route('/profile')
def view_profile():
    # get db connection
    db = get_db()

    # fetch user
    try:
        # execute the SQL query
        user = db.execute(
            "SELECT * FROM User WHERE id=?;", (session['uid'],)).fetchone()

        # if the user was found
        if user:
            # redirect to index
            return render_template('profile/profile.html', user=user)
        # if the user was not found
        else:
            # render the login page with an error message
            return redirect("/404")
    except sqlite3.Error as er:
        print('SQLite error: %s' % (' '.join(er.args)))
        return redirect("/404")


@bp.route('/edit/profile', methods=['GET', 'POST'])
def edit_profile():
    # get db connection
    db = get_db()

    # fetch user
    try:
        # execute the SQL query
        user = db.execute(
            "SELECT * FROM User WHERE id=?;", (session['uid'],)).fetchone()

        # if the user was found
        if user:
            if request.method == 'GET':
                # redirect to index
                return render_template('profile/edit-profile.html', user=user)
            else:
                email = request.form['email']
                first_name = request.form['first-name']
                last_name = request.form['last-name']
                birthdate = request.form['birthdate']
                avatarURL = request.form['avatarURL']
                address = request.form['address']

                db.execute(
                    "UPDATE User SET email=?, first_name=?, last_name=?, birthdate=?, avatarURL=?, address=? WHERE id=?;", (email, first_name, last_name, birthdate, avatarURL, address, session['uid'],)).fetchone()

                db.commit()
                return redirect(url_for('profile.view_profile'))
        # if the user was not found
        else:
            # render the login page with an error message
            return redirect("/404")
    except sqlite3.Error as er:
        print('SQLite error: %s' % (' '.join(er.args)))
        return redirect("/404")


@bp.route('/delete/profile')
def delete_profile():

    # get db connection
    db = get_db()

    # fetch user
    try:
        # execute the SQL query
        db.execute("DELETE FROM User WHERE id=?;", (session['uid'],))
        db.commit()

        return redirect(url_for("login.logout"))

    except sqlite3.Error as er:
        print('SQLite error: %s' % (' '.join(er.args)))
        return redirect("/404")


@bp.route('/password_change', methods=["GET", "POST"])
def user_password_change():

    #read values in form
    if request.method=='GET':
        return render_template('profile/change_password.html')

    else:
        current_password=request.form['current_password']
        new_password=request.form['new_password']
        repeat_password=request.form['repeat_password']

        

        # get db connection
        db = get_db()

        # fetch user
        try:
            # execute the SQL query
            user = db.execute(
                "SELECT password FROM User WHERE id=?;", (session['uid'],)).fetchone()

                
            # print(current_password,new_password,repeat_password)
            # print(password['password'])

            # if the password is equal current password
            if current_password == user['password']  and new_password ==repeat_password:

                #update password
                db.execute(
                "UPDATE User SET password=? WHERE id=?;", (new_password, session['uid'],))
                db.commit()
                #render the password page  the user
                return render_template('profile/change_password.html' , message='password succesful change')

                    
                
            # if the password was incorrect
            else:
                # render the change password page with an error message
                return render_template('profile/change_password.html' , message='password not change')

            
        except sqlite3.Error as er:
            print('SQLite error: %s' % (' '.join(er.args)))
            return redirect("/404")




            


  




        
 
    return render_template('change_password.html', form=form)