import sys

import random, json
from flask import *
from flask_cors import *
import App
from models.DatabaseContext import *

@App.app.route('/')
def login_page():
    if session.get("user_id") is not None and session.get("fullname") is not None:
        return render_template('Home/Home.html')
    else:
        return render_template('Home/Index.html')

@App.app.route('/Dashboard')
def dashboard_page():
    if session.get("user_id") is not None and session.get("fullname") is not None:
        return render_template('Home/Home.html')
    else:
        return render_template('Home/Index.html')