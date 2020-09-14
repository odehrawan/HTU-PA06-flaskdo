import sqlite3
from flask import Blueprint, render_template, request, redirect, session, url_for
from ..db import get_db
from datetime import datetime


# define our blueprint
bp = Blueprint('task_list', __name__)


@bp.route('/mylists', methods=['GET'])
def mylists():
   
    # get the db connection
    db = get_db()

    # insert user into db
    try:
        # execute the SQL query
        mylists = db.execute(
            "SELECT * FROM TaskList WHERE user_id=?;", (str(session['uid']))).fetchall()
        return render_template('task-lists/task-lists.html', mylists=mylists )

    except sqlite3.Error as er:
        print('SQLite error: %s' % (' '.join(er.args)))
        return redirect("/404")


@bp.route('/add/list', methods=['GET', 'POST'])
def add_list():
    if request.method == 'GET':
        return render_template('task-lists/add-task-list.html')
    else:
        list_name = request.form['list-name']
        list_description = request.form['list-description']
        user_id = session['uid']

      
       
        


        # get the db connection
        db = get_db()

        # insert user into db
        try:
            # execute the SQL query
            db.execute(
                "INSERT INTO TaskList (name, description, user_id) VALUES (?, ?, ?);", (list_name, list_description, user_id))

            # commit the changes to the DB
            db.commit()

            return redirect('/mylists')
        except sqlite3.Error as er:
            print('SQLite error: %s' % (' '.join(er.args)))
            return redirect("/404")


@bp.route('/update/list/<int:tasklist_id>', methods=['GET', 'POST'])
def update_list(tasklist_id):
    # get db connection
    db = get_db()

    # fetch task list
    try:
        # execute the SQL query
        tasklist = db.execute(
            "SELECT * FROM TaskList WHERE id=? AND user_id=?;", (tasklist_id, session['uid'])).fetchone()

        # if the tasklist was found
        if tasklist:

            if request.method == 'GET':
                # render the update list form with pre-populated values
                return render_template('task-lists/update-list.html', tasklist=tasklist)
            else:

                # read the values from the update list form
                name = request.form['list-name']
                description = request.form['list-description']

                # execute the SQL query
                db.execute(
                    "UPDATE TaskList SET name=?, description=? WHERE id=?;", (name, description, tasklist_id))

                # write changes to the DB
                db.commit()

                # redirect to the 'view_list' view
                return redirect(url_for('task_list.view_list', tasklist_id=tasklist_id))

        # if the tasklist was not found
        else:
            # redirect to 404
            return redirect("/404")

    except sqlite3.Error as er:
        print('SQLite error: %s' % (' '.join(er.args)))
        return redirect("/403")


@bp.route('/list/<int:tasklist_id>')
def view_list(tasklist_id):

    # find the task list

    # get db connection
    db = get_db()

    # fetch task list
    try:
        # execute the SQL query
        tasklist = db.execute(
            "SELECT * FROM TaskList WHERE id=? AND user_id=?;", (tasklist_id, session['uid'])).fetchone()

        # if the tasklist was found
        if tasklist:
            tl_name = tasklist['name']
            tl_description = tasklist['description']

            # execute the SQL query
            tasks = db.execute(
                "SELECT * FROM Task WHERE task_list_id=?;", (tasklist_id,)).fetchall()

            # render_template to 'task-list'
            return render_template('task-lists/task-list.html', tl_name=tl_name, tl_description=tl_description, tasks=tasks)

        # if the tasklist was not found
        else:
            # redirect to 404
            return redirect("/404")

    except sqlite3.Error as er:
        print('SQLite error: %s' % (' '.join(er.args)))
        return redirect("/404")


@bp.route('/delete/list/<int:tasklist_id>')
def delete_list(tasklist_id):
    # get db connection
    db = get_db()

    # fetch task list
    try:
        # execute the SQL query
        tasklist = db.execute(
            "SELECT * FROM TaskList WHERE id=? AND user_id=?;", (tasklist_id, session['uid'])).fetchone()

        # if the tasklist was found
        if tasklist:
            # execute the SQL query
            db.execute("DELETE FROM TaskList WHERE id=?;", (tasklist_id,))

            # write changes to the DB
            db.commit()

            # redirect to the 'view_list' view
            return redirect(url_for('task_list.mylists'))

        # if the tasklist was not found
        else:
            # redirect to 404
            return redirect("/404")

    except sqlite3.Error as er:
        print('SQLite error: %s' % (' '.join(er.args)))
        return redirect("/404")
