import sys
import logging
from flask import session
from datetime import datetime


def InsertInfoLog(logType, entityTitle, entityName, data, ID):
    logging.basicConfig(filename='config/logHistory.log',level=logging.DEBUG)
    log = logging.getLogger('werkzeug')
    log.disabled = True
    if entityName is not None and ID is not None:
        if logType == 'create':
            logging.info("[" + datetime.now().strftime('%Y/%m/%d %H:%M:%S') + "] - New " + entityTitle + " was created by " + session['fullname'] + " with this data: " + str(data['objects'][entityName][ID]))
        elif logType == 'delete':
            logging.info("[" + datetime.now().strftime('%Y/%m/%d %H:%M:%S') + "] - " + entityTitle + " was deleted by " + session['fullname'] + " with this data: " + str(data['objects'][entityName][ID]))
        elif logType == 'update':
            logging.info("[" + datetime.now().strftime('%Y/%m/%d %H:%M:%S') + "] - " + entityTitle + " was updated by " + session['fullname'] + " with this data: " + str(data['objects'][entityName][ID]))
    else:
        if logType == 'create':
            logging.info("[" + datetime.now().strftime('%Y/%m/%d %H:%M:%S') + "] - New " + entityTitle + " was created by " + session['fullname'] + " with this data: " + str(data))
        elif logType == 'delete':
            logging.info("[" + datetime.now().strftime('%Y/%m/%d %H:%M:%S') + "] - " + entityTitle + " was deleted by " + session['fullname'] + " with this data: " + str(data))
        elif logType == 'update':
            logging.info("[" + datetime.now().strftime('%Y/%m/%d %H:%M:%S') + "] - " + entityTitle + " was updated by " + session['fullname'] + " with this data: " + str(data))

def InsertErrorLog(entityTitle, methodName):
    logging.basicConfig(filename='config/logHistory.log',level=logging.DEBUG)
    log = logging.getLogger('werkzeug')
    log.disabled = True
    logging.error("[" + datetime.now().strftime('%Y/%m/%d %H:%M:%S') + "] - An exception occurred during " + methodName + " of "+ entityTitle +" by " + session['fullname'], exc_info=True)