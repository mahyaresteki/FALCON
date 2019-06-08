import sys
import random, json
from psycopg2 import connect
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import pymysql
from flask import *
from flask_cors import CORS, cross_origin
import App
from models.DatabaseContext import *
import hashlib
import configparser
from datetime import datetime

@App.app.route('/Home/Login', methods=['GET', 'POST'])
@cross_origin(supports_credentials=True)
def Login():
    with db_session:
        data = request.get_json()
        username = str(data['username'])
        password = hashlib.sha512(str(data['password']).encode('utf-8')).hexdigest()
        query = Users.select(lambda u: u.Username == str(username) and u.Password == str(password))
        mylist = list(query)
        message=""
        if len(mylist) > 0:
            if mylist[0].IsActive : 
                message = "Success"
                query2 = list(RoleAccesses.select(lambda ra: ra.RoleID == mylist[0].RoleID))
                result = '{'
                for r in query2[:-1]:
                    result += '"' + r.AppFormID.AppFormTitle + '" : "' + str(r.ReadGrant)+'", '
                result += '"' + query2[-1].AppFormID.AppFormTitle + '" : "' + str(query2[-1].ReadGrant) + '"'
                result += '}'
                session["user_id"] = mylist[0].UserID
                session["fullname"] = mylist[0].FirstName +' '+mylist[0].LastName
                session["menu_access"] = json.loads(str(result))
            else:
                message = "User is deactivated"
        else:
            message = "Username or password is incorrect"
        return jsonify({'message': message})


@App.app.route('/Home/SetDatabase', methods=['GET', 'POST'])
@cross_origin(supports_credentials=True)
def SetDatabase():
    data = request.get_json()
    if str(data['provider']) == 'postgres':
        con = connect(dbname='postgres', user=str(data['username']), host=str(data['host']), password=str(data['password']))
        con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = con.cursor()
        cur.execute('CREATE DATABASE ' + str(data['database']).lower())
        cur.close()
        con.close()
    elif str(data['provider']) == 'mysql':
        conn = pymysql.connect(host=str(data['host']), user=str(data['username']), password=str(data['password']))
        conn.cursor().execute('create database '+str(data['database']))
        conn.close()
    config = configparser.ConfigParser()
    config.sections()
    config.read('config/conf.ini')
    config.set('ConnectionString', 'provider', 'postgres')
    config.set('ConnectionString', 'host', str(data['host']))
    config.set('ConnectionString', 'database', str(data['database']).lower())
    config.set('ConnectionString', 'user', str(data['username']))
    config.set('ConnectionString', 'password', str(data['password']))
    with open('config/conf.ini', 'w') as configfile:
        config.write(configfile)
    db.bind(provider=config['ConnectionString']['provider'], user=config['ConnectionString']['user'], password=config['ConnectionString']['password'], host=config['ConnectionString']['host'], database=config['ConnectionString']['database'])
    db.generate_mapping(create_tables=True)
    with db_session:
        AppForms(AppFormTitle='Roles')
        AppForms(AppFormTitle='Role Accesses')
        AppForms(AppFormTitle='Users')
        AppForms(AppFormTitle='Settings')
        AppForms(AppFormTitle='Leaves')
        AppForms(AppFormTitle='Hour Off Leave')
        AppForms(AppFormTitle='Leave Approval')
        AppForms(AppFormTitle='Transport Types')
        AppForms(AppFormTitle='Intra City Mission')
        AppForms(AppFormTitle='Out of City Mission')
        AppForms(AppFormTitle='Mission Approval')
    message = "Success"
    return jsonify({'message': message})

@App.app.route('/Home/SetAdministrator', methods=['GET', 'POST'])
@cross_origin(supports_credentials=True)
def SetAdministrator():
    data = request.get_json()
    with db_session:
        Roles(RoleTitle = 'Administrator', LatestUpdateDate = datetime.now())
        roleId = list(Roles.select(lambda u: u.RoleTitle == 'Administrator'))[0].RoleID
        appforms = AppForms.select()
        appformslist = list(appforms)
        for item in appformslist:
            RoleAccesses(RoleID = roleId, AppFormID = item.AppFormID , CreateGrant = True, ReadGrant=True, UpdateGrant=True, DeleteGrant=True, PrintGrant=True, LatestUpdateDate = datetime.now())
        
        password = hashlib.sha512(str(data['Password']).encode('utf-8')).hexdigest()
        Users(FirstName = str(data['FirstName']), LastName =str(data['LastName']), Username=str(data['Username']), Password=password, RoleID=roleId, PersonelCode=str(data['PersonelCode']), IsActive=True, LatestUpdateDate = datetime.now() )
    message = "Success"
    return jsonify({'message': message})

@App.app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('fullname', None)
    return redirect("/", code=302)

def CheckAccess(appFormTitle, accessType):
    with db_session:
        user = list(Users.select(lambda u: u.UserID == int(session["user_id"])))
        roleAccess = list(RoleAccesses.select(lambda ra: ra.RoleID == user[0].RoleID and ra.AppFormID.AppFormTitle == str(appFormTitle)))
        if accessType == 'Read':
            return roleAccess[0].ReadGrant
        elif accessType == 'Create':
            return roleAccess[0].CreateGrant
        elif accessType == 'Update':
            return roleAccess[0].UpdateGrant 
        elif accessType == 'Delete':
            return roleAccess[0].DeleteGrant
        else:
            return roleAccess[0].PrintGrant

def GetFormAccessControl(appFormTitle):
    user = list(Users.select(lambda u: u.UserID == int(session["user_id"])))
    roleAccess = list(RoleAccesses.select(lambda ra: ra.RoleID == user[0].RoleID and ra.AppFormID.AppFormTitle == str(appFormTitle)))
    result = '{"Read": "'+ str(roleAccess[0].ReadGrant) +'", "Create":"'+ str(roleAccess[0].CreateGrant) +'", "Update":"'+ str(roleAccess[0].UpdateGrant) +'", "Delete":"'+ str(roleAccess[0].DeleteGrant) +'", "Print":"'+ str(roleAccess[0].PrintGrant) +'"}'
    return json.loads(str(result))