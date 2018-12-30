import sys

import random, json
from flask import *
from flask_cors import CORS, cross_origin
import App
from models.DatabaseContext import *
import hashlib

@App.app.route('/Home/Login', methods=['GET', 'POST'])
@cross_origin(supports_credentials=True)
def Login():
    with db_session:
        data = request.get_json()
        username = str(data['username'])
        password = hashlib.sha512(str(data['password']).encode('utf-8')).hexdigest()
        query= Users.select(lambda u: u.Username == str(username) and u.Password == str(password))
        mylist = list(query)
        message=""
        if len(mylist) > 0:
            if mylist[0].IsActive : 
                message = "Success"
                session["user_id"] = mylist[0].UserID
                session["fullname"] = mylist[0].FirstName +' '+mylist[0].LastName
            else:
                message = "User is deactivated"
        else:
            message = "Username or password is incorrect"
        return jsonify({'message': message})


@App.app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('fullname', None)
    return render_template('Home/Index.html')