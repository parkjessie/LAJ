""" database dependencies to support Users db examples """
from __init__ import db
import csv
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import os
import shutil
from random import randrange

# Tutorial: https://www.sqlalchemy.org/library.html#tutorials, try to get into Python shell and follow along

# Define the Users table within the model
# -- Object Relational Mapping (ORM) is the key concept of SQLAlchemy
# -- a.) db.Model is like an inner layer of the onion in ORM
# -- b.) Users represents data we want to store, something that is built on db.Model
# -- c.) SQLAlchemy ORM is layer on top of SQLAlchemy Core, then SQLAlchemy engine, SQL

# Define the 'Users Notes' table  with a relationship to Users within the model
class Notes(db.Model):
    __tablename__ = 'notes'

    # Define the Notes schema
    id = db.Column(db.Integer, primary_key=True)
    note = db.Column(db.Text, unique=False, nullable=False)
    # Define a relationship in Notes Schema to userID who originates the note, many-to-one (many notes to one user)
    userID = db.Column(db.Integer, db.ForeignKey('users.userID'))

    # Constructor of a Notes object, initializes of instance variables within object
    def __init__(self, note, userID):
        self.note = note
        self.userID = userID

    # Returns a string representation of the Notes object, similar to java toString()
    # returns string
    def __repr__(self):
        return "Notes(" + str(self.id) + "," + self.note + "," + str(self.userID) + ")"

    # CRUD create, adds a new record to the Notes table
    # returns the object added or None in case of an error
    def create(self):
        try:
            # creates a Notes object from Notes(db.Model) class, passes initializers
            db.session.add(self)  # add prepares to persist person object to Notes table
            db.session.commit()  # SqlAlchemy "unit of work pattern" requires a manual commit
            return self
        except IntegrityError:
            db.session.remove()
            return None

    # CRUD read, returns dictionary representation of Notes object
    # returns dictionary
    def read(self):
        return {
            "id": self.id,
            "note": self.note,
            "userID": self.userID
        }


def load_data():
    db.create_all()
    # got the database from admin and then converted it into a csv file
    data = "courses.csv"
    # takes csv file and stores data into a variable
    with open(data, newline='') as f:
        reader = csv.reader(f)
        results = list(reader)
    # results.remove(0)
    # takes data and makes each result a separate row in the database
    for index, result in enumerate(results):
        # skips first and last row so that database doesn't include headers or totals from csv
        if index != 0 and index != len(results) - 1:
            c = Courses(result)  # takes a row out of results
            c.create()  # creates a row in the database
    courses = Courses.query
    for course in courses:
        print(course.read())


class Courses(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dept = db.Column(db.String)
    title = db.Column(db.String)
    courseid = db.Column(db.String, unique=True, nullable=False)
    ninth = db.Column(db.String)
    tenth = db.Column(db.String)
    eleventh = db.Column(db.String)
    twelfth = db.Column(db.String)
    notes = db.Column(db.String)

    def __init__(self, result):
        self.dept = result[0]
        self.title = result[1]
        self.courseid = result[2]
        self.ninth = result[3]
        self.tenth = result[4]
        self.eleventh = result[5]
        self.twelfth = result[6]
        self.notes = result[7]

    def create(self):
        try:
            # creates a person object from Users(db.Model) class, passes initializers
            db.session.add(self)  # add prepares to persist person object to Users table
            db.session.commit()  # SqlAlchemy "unit of work pattern" requires a manual commit
            return self
        except IntegrityError:
            db.session.remove()
            return None

    def read(self):
        return {
            "department": self.dept,
            "course_name": self.title,
            "course_id": self.courseid,
            "freshman": self.ninth,
            "sophomore": self.tenth,
            "junior": self.eleventh,
            "senior": self.twelfth,
            "notes": self.notes
        }

def model_printer():
    print("------------")
    print("Table: users with SQL query")
    print("------------")
    result = db.session.execute('select * from Courses')
    print(result.keys())
    for row in result:
        print(row)


class Users(UserMixin, db.Model):
    # define the Users schema
    userID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=False, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), unique=False, nullable=False)
    phone = db.Column(db.String(255), unique=False, nullable=False)

    notes = db.relationship("Notes", cascade='all, delete', backref='users', lazy=True)

    # constructor of a User object, initializes of instance variables within object
    def __init__(self, name, email, password, phone):
        self.name = name
        self.email = email
        self.set_password(password)
        self.phone = phone

    # CRUD create/add a new record to the table
    # returns self or None on error
    def create(self):
        try:
            # creates a person object from Users(db.Model) class, passes initializers
            db.session.add(self)  # add prepares to persist person object to Users table
            db.session.commit()  # SqlAlchemy "unit of work pattern" requires a manual commit
            return self
        except IntegrityError:
            db.session.remove()
            return None

    # CRUD read converts self to dictionary
    # returns dictionary
    def read(self):
        return {
            "userID": self.userID,
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "phone": self.phone,
            "query": "by_alc"  # This is for fun, a little watermark
        }

    # CRUD update: updates users name, password, phone
    # returns self
    def update(self, name, password="", phone=""):
        """only updates values with length"""
        if len(name) > 0:
            self.name = name
        if len(password) > 0:
            self.set_password(password)
        if len(phone) > 0:
            self.phone = phone
        db.session.commit()
        return self

    # CRUD delete: remove self
    # None
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return None

    # set password method is used to create encrypted password
    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password, method='sha256')

    # check password to check versus encrypted password
    def is_password_match(self, password):
        """Check hashed password."""
        result = check_password_hash(self.password, password)
        return result

    # required for login_user, overrides id (login_user default) to implemented userID
    def get_id(self):
        return self.userID


"""Database Creation and Testing section"""


def model_builder():
     print("--------------------------")
     print("Seed Data for Table: users")
     print("--------------------------")
     db.create_all()
     """Tester data for table"""
     u1 = Users(name='Thomas Edison', email='tedison@example.com', password='123toby', phone="1111111111")
     u2 = Users(name='Nicholas Tesla', email='ntesla@example.com', password='123niko', phone="1111112222")
     u3 = Users(name='Alexander Graham Bell', email='agbell@example.com', password='123lex', phone="1111113333")
     u4 = Users(name='Eli Whitney', email='eliw@example.com', password='123whit', phone="1111114444")
     u5 = Users(name='John Mortensen', email='jmort1021@gmail.com', password='123qwerty', phone="8587754956")
     u6 = Users(name='John Mortensen', email='jmort1021@yahoo.com', password='123qwerty', phone="8587754956")
     # U7 intended to fail as duplicate key
     u7 = Users(name='John Mortensen', email='jmort1021@yahoo.com', password='123qwerty', phone="8586791294")

     table = [u1, u2, u3, u4, u5, u6, u7]
     for row in table:
    # prime uploads foler
        try:
            os.makedirs('../volumes/uploads')
        except:
            pass
        #shutil.copy("../static/assets/ncs_logo.png", "../volumes/uploads")
        # add some notes with default image
        try:
            '''add a few 1 to 4 notes per user'''
            for num in range(randrange(1, 4)):
                note = "#### " + row.name + " note " + str(num) + ". \n Generated by test data."
                row.notes.append(Notes(userID=row.userID, note=note))
            '''add user/note data to table'''
            db.session.add(row)
            db.session.commit()
        except IntegrityError:
            '''fails with bad or duplicate data'''
            db.session.remove()
            print(f"Records exist, duplicate email, or error: {row.email}")



# Looks into database
def model_driver():
    print("---------------------------")
    print("Create Tables and Seed Data")
    print("---------------------------")
    model_builder()

    print("---------------------------")
    print("Table: " + Users.__tablename__)
    print("Columns: ", Users.__table__.columns.keys())
    print("---------------------------")
    print("Table: " + Notes.__tablename__)
    print("Columns: ", Notes.__table__.columns.keys())
    print("---------------------------")
    print()

    users = Users.query
    for user in users:
        print("User" + "-" * 81)
        print(user.read())
        print("Notes" + "-" * 80)
        for note in user.notes:
            print(note.read())
        print("-" * 85)
        print()


if __name__ == "__main__":
    model_driver()
