import sys
import time

try:
    from pip import main as pipmain
except ImportError:
    from pip._internal import main as pipmain

try:
    from flask import Flask, request, jsonify
    from flask_cors import CORS, cross_origin
    from flask_paginate import Pagination, get_page_parameter
    import numpy
    import xlsxwriter
    import pandas
    from pony.orm import *
    from PollyReports import *
    import psycopg2
    import pymysql
    import reportlab
    pymysql.install_as_MySQLdb()
    
except ImportError:
    pipmain(['install', 'flask', 'pony', 'flask-cors', 'psycopg2', 'pymysql', 'numpy', 'flask-paginate', 'XlsxWriter', 'pandas', 'PollyReports', 'reportlab'])

import configparser
import random, threading, webbrowser
from datetime import datetime
from models.DatabaseContext import *
from App import *
import controllers.Security
import controllers.Home
import controllers.UserManagement
import controllers.LeaveManagement
import controllers.TransportTypeManagement
import controllers.MissionManagement
import controllers.SettingsManagement



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
    