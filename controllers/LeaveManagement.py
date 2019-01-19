import sys
import random, json
from pony import orm
from flask import *
from flask_cors import *
import App
from models.DatabaseContext import *
import hashlib
from datetime import datetime

@App.app.route('/LeaveManagement/Leaves')
def leave_page():
    if session.get("user_id") is not None and session.get("fullname") is not None:
        with db_session:
            myleaves = Leaves.select(lambda l: l.UserID.UserID == int(session.get("user_id")))
            return render_template('LeaveManagement/Leaves.html', myleaves = myleaves)
    else:
        return redirect("/", code=302)