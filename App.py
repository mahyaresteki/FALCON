import sys
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin

global app
app = Flask(__name__)
app.config.from_object(__name__)
CORS(app, support_credentials=True)