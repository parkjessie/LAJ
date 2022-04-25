from flask import render_template
from __init__ import app
from crudy.app_crud import app_crud
from crudy.app_crud_api import app_crud_api

app.register_blueprint(app_crud)
app.register_blueprint(app_crud_api)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/registration')
def registration():
    return render_template("layouts/registration.html")


if __name__ == "__main__":
    # runs the application on the repl development server
    app.run(debug=True, port="5003")
