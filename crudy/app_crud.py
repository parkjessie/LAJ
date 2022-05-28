"""control dependencies to support CRUD app routes and APIs"""
from flask import Blueprint, render_template, request, url_for, redirect, jsonify, make_response, app
from flask_login import login_required

from crudy.query import *

# blueprint defaults https://flask.palletsprojects.com/en/2.0.x/api/#blueprint-objects
app_crud = Blueprint('crud', __name__,
                     url_prefix='/crud',
                     template_folder='templates/cruddy/',
                     static_folder='static',
                     static_url_path='static')

""" Blueprint is established to isolate Application control code for CRUD operations, key features:
    1.) 'Users' table control methods, controls relationship between User Actions and Database Model
    2.) Control methods are achieved using app routes for each CRUD operations
    3.) login required to restrict CRUD operations to identified users
"""

# mysql = MySQL()
#
# # configuring MySQL for the web application
# app.config['MYSQL_DATABASE_USER'] = 'root'    # default user of MySQL to be replaced with appropriate username
# app.config['MYSQL_DATABASE_PASSWORD'] = '' # default passwrod of MySQL to be replaced with appropriate password
# app.config['MYSQL_DATABASE_DB'] = 'jobsdb'  # Database name to be replaced with appropriate database name
# app.config['MYSQL_DATABASE_HOST'] = 'localhost' # default database host of MySQL to be replaced with appropriate database host
# #initialise mySQL
# mysql.init_app(app)
# #create connection to access data
# conn = mysql.connect()

@app_crud.route('/fouryearplanner')
def fouryearplanner():
    subjects_list = courses_english(["SSCI", "ENGL", "MATH", "SCI", "FLNG", "ELEC", "PE", "OFF ROLL"])
    return render_template("fouryearplanner.html", subjects_titles=subjects_list[0], subjects_list=subjects_list[1])


# Default URL for Blueprint
@app_crud.route('/')
# @login_required  # Flask-Login uses this decorator to restrict acess to logged in users
def crud():
    """obtains all Users from table and loads Admin Form"""
    return render_template("crud.html", table=courses_all())


# Flask-Login directs unauthorised users to this unauthorized_handler
@login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized users to Login page."""
    return redirect(url_for('crud.crud_login'))


# if login url, show phones table only
@app_crud.route('/login/', methods=["GET", "POST"])
def crud_login():
    # obtains form inputs and fulfills login requirements
    if request.form:
        email = request.form.get("email")
        password = request.form.get("password")
        phone = request.form.get("phone")
        if login(email, password, phone):       # zero index [0] used as email is a tuple
            return redirect(url_for('crud.crud'))

    # if not logged in, show the login page
    return render_template("login.html")


@app_crud.route('/authorize/', methods=["GET", "POST"])
def crud_authorize():
    # check form inputs and creates user
    if request.form:
        # validation should be in HTML
        user_name = request.form.get("user_name")
        email = request.form.get("email")
        password1 = request.form.get("password1")
        password2 = request.form.get("password1")           # password should be verified
        phone = request.form.get("phone")
        if authorize(user_name, email, password1, phone):    # zero index [0] used as user_name and email are type tuple
            return redirect(url_for('crud.crud_login'))
    # show the auth user page if the above fails for some reason
    return render_template("authorize.html")

@app_crud.route('/logout')
@login_required
def logout():
    logout_user() # logs user out
    print("logged out") # error checking to ensure log out happened
    return redirect("/")
    # check if logged in
    # if logged in, log out

# CRUD create/add
@app_crud.route('/create/', methods=["POST"])
def create():
    """gets data from form and add it to Users table"""
    if request.form:
        po = user(
            request.form.get("name"),
            request.form.get("email"),
            request.form.get("password"),
            request.form.get("phone")
        )
        po.create()
    return redirect(url_for('crud.crud'))


# CRUD read
@app_crud.route('/read/', methods=["POST"])
def read():
    """gets userid from form and obtains corresponding data from Users table"""
    table = []
    if request.form:
        userid = request.form.get("userid")
        po = user_by_id(userid)
        if po is not None:
            table = [po.read()]  # placed in list for easier/consistent use within HTML
    return render_template("crud.html", table=table)


# CRUD update
@app_crud.route('/update/', methods=["POST"])
def update():
    """gets userid and name from form and filters and then data in  Users table"""
    if request.form:
        userid = request.form.get("userid")
        name = request.form.get("name")
        po = user_by_id(userid)
        if po is not None:
            po.update(name)
    return redirect(url_for('crud.crud'))


# CRUD delete
@app_crud.route('/delete/', methods=["POST"])
def delete():
    """gets userid from form delete corresponding record from Users table"""
    if request.form:
        userid = request.form.get("userid")
        po = user_by_id(userid)
        if po is not None:
            po.delete()
    return redirect(url_for('crud.crud'))


# Search Form
@app_crud.route('/search/')
#@login_required
def search():
    """loads form to search Users data"""
    return render_template("search.html")


# Search request and response
@app_crud.route('/search/term/', methods=["POST"])
def search_term():
    """ obtain term/search request """
    req = request.get_json()
    term = req['term']
    response = make_response(jsonify(users_ilike(term)), 200)
    return response