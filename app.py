from flask import Flask, render_template, request
import requests
import json
import random
from __init__ import app

@app.route('/')
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)