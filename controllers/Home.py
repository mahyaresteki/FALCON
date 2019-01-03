import sys

import random, json
from flask import *
from flask_cors import *
import App
from models.DatabaseContext import *

@App.app.route('/')
def login_page():
    if session.get("user_id") is not None and session.get("fullname") is not None:
        return redirect("/Dashboard", code=302)
    else:
        with db_session:
            query= Users.select()
            mylist = list(query)
            if len(mylist) > 0:
                return render_template('Home/index.html')
            else:
                return redirect("/Setup?step=admin", code=302)

@App.app.route('/Dashboard')
def dashboard_page():
    if session.get("user_id") is not None and session.get("fullname") is not None:
        return render_template('Home/home.html')
    else:
        return redirect("/", code=302)

@App.app.route('/Setup')
def setup_page():
    return render_template('Home/setup.html')