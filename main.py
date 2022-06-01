from flask import render_template
from flask_login import login_required

from __init__ import app
from crudy.app_crud import app_crud
from crudy.app_crud_api import app_crud_api
from crudy.app_notes import app_notes

app.register_blueprint(app_crud)
app.register_blueprint(app_crud_api)
app.register_blueprint(app_notes)


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/fouryearplan')
def fouryearplan():
    return render_template("fouryearplan.html")

@app.route('/info')
def info():
    return render_template("info.html")

@app.route('/math')
def math():
    return render_template("math.html")

@app.route('/courseselection')
def courseselection():
    return render_template("courseselection.html")

if __name__ == "__main__":
    # runs the application on the repl development server
    app.run(debug=True, port="5005")
