from pony.orm import *
from App import *
from models.DatabaseContext import *
import controllers.Security
import controllers.Home
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin

if __name__ == "__main__":
    app.secret_key = 'falcon'
    app.config['SESSION_TYPE'] = 'filesystem'

    app.debug = True
    db.generate_mapping(create_tables=True)
    app.run(host='127.0.0.1', port=5000)