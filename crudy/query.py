from __init__ import login_manager, db
from crudy.model import Users, Courses
from flask_login import current_user, login_user, logout_user


def courses_all():
    table = Courses.query.all()
    json_ready = [course.read() for course in table]
    return json_ready


def courses_with_repeats(has_repeats):
    table = Courses.query.filter_by(dept=has_repeats)
    json_ready = [course.read() for course in table]

    freshman = []
    for j in json_ready:
        if j["freshman"] != "":
            freshman.append(j)

    sophomore = []
    for j in json_ready:
        if j["sophomore"] != "":
            sophomore.append(j)

    junior = []
    for j in json_ready:
        if j["junior"] != "":
            junior.append(j)

    senior = []
    for j in json_ready:
        if j["senior"] != "":
            senior.append(j)
    return freshman, sophomore, junior, senior


def courses_english(subjects):
    # table = Courses.query.all()
    subject_titles = []
    subject_courses = []
    for subject in subjects:
        table = Courses.query.filter_by(dept=subject)
        json_ready = [course.read() for course in table]

        freshman = []
        for j in json_ready:
            if j["freshman"] != "":
                freshman.append(j)

        sophomore = []
        for j in json_ready:
            if j["sophomore"] != "":
                sophomore.append(j)

        junior = []
        for j in json_ready:
            if j["junior"] != "":
                junior.append(j)

        senior = []
        for j in json_ready:
            if j["senior"] != "":
                senior.append(j)

        subject_titles.append(subject)
        subject_courses.append([freshman, sophomore, junior, senior])
    # subjects_list.append([{"subject_courses": subject_courses}])
    return [subject_titles, subject_courses]


# this is method called by frontend, it has been randomized between Alchemy and Native SQL for fun
def users_all():
    """  May have some problems with sql in deployment
    if random.randint(0, 1) == 0:
        table = users_all_alc()
    else:
        table = users_all_sql()
    return table
    """

    return users_all_alc()


# SQLAlchemy extract all users from database
def users_all():
    table = Users.query.all()
    json_ready = [peep.read() for peep in table]
    return json_ready


# Native SQL extract all users from database
def users_all_sql():
    table = db.session.execute('select * from users')
    json_ready = sqlquery_2_list(table)
    return json_ready


# ALGORITHM to convert the results of an SQL Query to a JSON ready format in Python
def sqlquery_2_list(rows):
    out_list = []
    keys = rows.keys()  # "Keys" are the columns of the sql query
    for values in rows:  # "Values" are rows within the SQL database
        row_dictionary = {}
        for i in range(len(keys)):  # This loop lines up K, V pairs, same as JSON style
            row_dictionary[keys[i]] = values[i]
        row_dictionary["query"] = "by_sql"  # This is for fun a little watermark
        out_list.append(row_dictionary)  # Finally we have a out_list row
    return out_list


# SQLAlchemy extract users from database matching term
def users_ilike(term):
    """filter Users table by term into JSON list (ordered by User.name)"""
    term = "%{}%".format(term)  # "ilike" is case insensitive and requires wrapped  %term%
    table = Users.query.order_by(Users.name).filter((Users.name.ilike(term)) | (Users.email.ilike(term)))
    return [peep.read() for peep in table]


# SQLAlchemy extract single user from database matching ID
def user_by_id(userid):
    """finds User in table matching userid """
    return Users.query.filter_by(userID=userid).first()


# SQLAlchemy extract single user from database matching email
def user_by_email(email):
    """finds User in table matching email """
    return Users.query.filter_by(email=email).first()


# check credentials in database
def is_user(email, password, phone):
    # query email and return user record
    user_record = user_by_email(email)
    # if user record found, check if password is correct
    return user_record and Users.is_password_match(user_record, password)


# login user based off of email and password
def login(email, password, phone):
    # sequence of checks
    if current_user.is_authenticated:  # return true if user is currently logged in
        return True
    elif is_user(email, password, phone):  # return true if email and password match
        user_row = user_by_email(email)
        login_user(user_row)  # sets flask login_user
        return True
    else:  # default condition is any failure
        return False


# this function is needed for Flask-Login to work.
@login_manager.user_loader
def user_loader(user_id):
    """Check if user login status on each page protected by @login_required."""
    if user_id is not None:
        return Users.query.get(user_id)
    return None


# Authorise new user requires user_name, email, password
def authorize(name, email, password, phone):
    if is_user(email, password, phone):
        return False
    else:
        auth_user = Users(
            name=name,
            email=email,
            password=password,
            phone=phone,  # this should be added to authorize.html
        )
        # encrypt their password and add it to the auth_user object
        auth_user.create()
        return True


# logout user
def logout():
    logout_user()  # removes login state of user from session


