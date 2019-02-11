from pony.orm import *
from App import *
from models.DatabaseContext import *
import controllers.Security
import controllers.Home
import controllers.UserManagement
import controllers.LeaveManagement
import controllers.TransportTypeManagement
import controllers.MissionManagement
import controllers.SettingsManagement
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import configparser
import random, threading, webbrowser

if __name__ == "__main__":
    app.debug = False
    app.secret_key = 'falcon'
    app.config['SESSION_TYPE'] = 'filesystem'
    config = configparser.ConfigParser()
    config.sections()
    config.read('config/conf.ini')

    if config['DEFAULT']['server'] == 'NotSet' or config['DEFAULT']['port'] == 'NotSet':
        print('')
        print('Falcon Leave Management Server')
        print('Application Installation Step')
        print('==================================')
        server = input('Please insert server IP address: ')
        port = input('Please insert port number: ')
        config.set('DEFAULT', 'server', server)
        config.set('DEFAULT', 'port', port)
        with open('config/conf.ini', 'w') as configfile:
            config.write(configfile)
    if config['ConnectionString']['host'] == 'NotSet' or config['ConnectionString']['database'] == 'NotSet':
        url = "http://{0}:{1}/Setup?step=database".format(config['DEFAULT']['server'],config['DEFAULT']['port'])
        threading.Timer(1.25, lambda: webbrowser.open(url) ).start()
    else:
        db.generate_mapping(create_tables=True)

    app.run(host=config['DEFAULT']['server'], port=config['DEFAULT']['port'])
    