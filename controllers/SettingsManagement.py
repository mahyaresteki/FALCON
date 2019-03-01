import os
import sys
import random, json
from flask import *
from flask_cors import CORS, cross_origin
import App
from models.SettingsModel import *
import configparser
from datetime import datetime
import numpy as np


@App.app.route('/SettingsManagement/Settings')
def settings_page():
    if session.get("user_id") is not None and session.get("fullname") is not None:
            hometownarea = np.loadtxt('config/hometownarea.txt', dtype=np.object)
            config = configparser.ConfigParser()
            config.sections()
            config.read('config/conf.ini')
            settings = SettingsModel(config['DEFAULT']['server'], config['DEFAULT']['port'], config['ConnectionString']['user'], config['ConnectionString']['password'], config['ConnectionString']['database'], config['ConnectionString']['host'], config['OrganizationInfo']['name'], config['OrganizationInfo']['latitude'], config['OrganizationInfo']['longitude']) 
            return render_template('SettingsManagement/Settings.html', settings = settings, hometown = hometownarea.tolist())
    else:
        return redirect("/", code=302)

@App.app.route('/SettingsManagement/SaveSettings', methods=['GET', 'POST'])
@cross_origin(supports_credentials=True)
def SaveSettings():
        try:
            if session.get("user_id") is not None and session.get("fullname") is not None:
                data = request.get_json()

                x = data['hometownArea']
                np.savetxt('config/hometownarea.txt', x, fmt='%s')

                config = configparser.ConfigParser()
                config.sections()
                config.read('config/conf.ini')
                currentServer = config['DEFAULT']['server']
                currentPort = config['DEFAULT']['port']
                config.set('DEFAULT', 'server', str(data['Server']))
                config.set('DEFAULT', 'port', str(data['Port']))
                config.set('ConnectionString', 'host', str(data['Host']))
                config.set('ConnectionString', 'database', str(data['Database']))
                config.set('ConnectionString', 'user', str(data['User']))
                config.set('ConnectionString', 'password', str(data['Password']))
                config.set('OrganizationInfo', 'name', str(data['OrganizationName']))
                config.set('OrganizationInfo', 'latitude', str(data['Latitude']))
                config.set('OrganizationInfo', 'longitude', str(data['Longitude']))
                with open('config/conf.ini', 'w') as configfile:
                    config.write(configfile)
                if currentServer != str(data['Server']) or currentPort != str(data['Port']):
                    os.execl(sys.executable, os.path.abspath(__file__), *sys.argv)
                else:
                    return 'success'
            else:
                return redirect("/", code=302)
        except Exception as e:
                message = str(e)
                return jsonify({'message': message})