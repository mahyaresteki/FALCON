import sys

import random, json
from flask import *
from flask_cors import *
import App
from models.DatabaseContext import *

@App.app.route('/UserManagement/Roles')
def role_page():
    if session.get("user_id") is not None and session.get("fullname") is not None:
        with db_session:
            roles = Roles.select()
            return render_template('UserManagement/roles.html', entries = roles)
    else:
        return redirect("/", code=302)