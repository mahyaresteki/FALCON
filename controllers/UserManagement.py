import sys
import random, json
from flask import *
from flask_cors import *
import App
from models.DatabaseContext import *
from datetime import datetime

@App.app.route('/UserManagement/Roles')
def role_page():
    if session.get("user_id") is not None and session.get("fullname") is not None:
        with db_session:
            roles = Roles.select()
            return render_template('UserManagement/roles.html', entries = roles)
    else:
        return redirect("/", code=302)

@App.app.route('/UserManagement/CreateRole', methods=['GET', 'POST'])
@cross_origin(supports_credentials=True)
def CreateRole():
    if session.get("user_id") is not None and session.get("fullname") is not None:
        with db_session:
            data = request.get_json()
            Roles(RoleTitle = data['RoleTitle'], Description = data['Description'], LatestUpdateDate = datetime.now())
            message = "Success"
            return jsonify({'message': message})
    else:
        return redirect("/", code=302)

@App.app.route('/UserManagement/GetRole', methods=['GET', 'POST'])
@cross_origin(supports_credentials=True)
def GetRole():
    if session.get("user_id") is not None and session.get("fullname") is not None:
        with db_session:
            data = request.get_json()
            query= Roles.select(lambda u: u.RoleID == int(data['RoleID']))
            mylist = list(query)
            return jsonify({'RoleID': mylist[0].RoleID, 'RoleTitle': mylist[0].RoleTitle, 'Description': mylist[0].Description})
    else:
        return redirect("/", code=302)


@App.app.route('/UserManagement/DeleteRole', methods=['GET', 'POST'])
@cross_origin(supports_credentials=True)
def DeleteRole():
    if session.get("user_id") is not None and session.get("fullname") is not None:
        with db_session:
            data = request.get_json()
            delete(p for p in Roles if p.RoleID == int(data["RoleID"]))
            message = "Success"
            return jsonify({'message': message})
    else:
        return redirect("/", code=302)
            