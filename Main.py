from pony.orm import *
from App import *
from models.DatabaseContext import *
import controllers.Security
import controllers.Home
import controllers.UserManagement
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

    
    if config['ConnectionString']['host'] == 'NotSet' or config['ConnectionString']['database'] == 'NotSet':
        url = "http://{0}:{1}/Setup?step=database".format(config['DEFAULT']['server'],config['DEFAULT']['port'])
        threading.Timer(1.25, lambda: webbrowser.open(url) ).start()
    else:
        db.generate_mapping(create_tables=True)

    app.run(host=config['DEFAULT']['server'], port=config['DEFAULT']['port'])
    