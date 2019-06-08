import sys

import random, json
from flask import *
from flask_cors import *
import App
from models.DatabaseContext import *
from models.AppInfoModel import *
import xml.etree.ElementTree as ET

@App.app.route('/')
def login_page():
    if session.get("user_id") is not None and session.get("fullname") is not None:
        return redirect("/Dashboard", code=302)
    else:
        with db_session:
            query= Users.select()
            mylist = list(query)
            if len(mylist) > 0:
                config = configparser.ConfigParser()
                config.sections()
                config.read('config/conf.ini')
                appinfo = AppInfoModel(config['AppInfo']['name'], config['AppInfo']['description'], config['AppInfo']['publisher'], config['AppInfo']['version'], config['AppInfo']['license'])
                return render_template('Home/index.html', appinfo = appinfo)
            else:
                return redirect("/Setup?step=admin", code=302)

@App.app.route('/Dashboard')
def dashboard_page():
    if session.get("user_id") is not None and session.get("fullname") is not None:
        return render_template('Home/dashboard.html')
    else:
        return redirect("/", code=302)

@App.app.route('/UserProfile')
def user_profile_page():
    if session.get("user_id") is not None and session.get("fullname") is not None:
         with db_session:
            query= Users.select(lambda u: u.UserID == int(session.get("user_id")))
            mylist = list(query)
            return render_template('Home/userprofile.html', user = mylist[0])
    else:
        return redirect("/", code=302)

@App.app.route('/About')
def about_page():
    if session.get("user_id") is not None and session.get("fullname") is not None:
        config = configparser.ConfigParser()
        config.sections()
        config.read('config/conf.ini')
        appinfo = AppInfoModel(config['AppInfo']['name'], config['AppInfo']['description'], config['AppInfo']['publisher'], config['AppInfo']['version'], config['AppInfo']['license'])
        mydoc = ET.parse('config/releases.xml') 
        releases = mydoc.getroot()
        return render_template('Home/about.html', appinfo = appinfo, releases = releases)
    else:
        return redirect("/", code=302)

@App.app.route('/Setup')
def setup_page():
    return render_template('Home/setup.html')

@App.app.route('/AccessDenied')
def access_denied_page():
    if session.get("user_id") is not None and session.get("fullname") is not None:
        return render_template('Home/accessdenied.html')
    else:
        return redirect("/", code=302)