import sys
import random, json
from pony import orm
from flask import *
from flask_cors import *
import App
from models.DatabaseContext import *
import hashlib
from datetime import datetime
import numpy as np
from controllers.Security import CheckAccess, GetFormAccessControl

@App.app.route('/MissionManagement/Missions')
def mission_page():
        if session.get("user_id") is not None and session.get("fullname") is not None:
                if CheckAccess("Intra City Mission", "Read"):
                        with db_session:
                                hometownarea = np.loadtxt('config/hometownarea.txt', dtype=np.object)
                                config = configparser.ConfigParser()
                                config.sections()
                                config.read('config/conf.ini')
                                mymissions = Missions.select(lambda l: l.UserID.UserID == int(session.get("user_id")))
                                transporttypes = TransportTypes.select()
                                return render_template('MissionManagement/Missions.html', mymissions = mymissions, transporttypes = transporttypes, orglat = config['OrganizationInfo']['latitude'], orglong = config['OrganizationInfo']['longitude'], hometown = hometownarea.tolist(), formAccess = GetFormAccessControl("Intra City Mission"))
                else:
                        return redirect("/AccessDenied", code=302)
        else:
                return redirect("/", code=302)

@App.app.route('/MissionManagement/CreateMission', methods=['GET', 'POST'])
@cross_origin(supports_credentials=True)
def CreateMission():
        try:
                if session.get("user_id") is not None and session.get("fullname") is not None:
                        if CheckAccess("Intra City Mission", "Create"):
                                with db_session:
                                        data = request.get_json()
                                        latitude = float(data['Latitude']) if data['Latitude']!='' else None
                                        longitude = float(data['Longitude']) if data['Longitude']!='' else None
                                        wentPayment = float(data['WentPayment']) if data['WentPayment']!='' else None
                                        returnPayment = float(data['ReturnPayment']) if data['ReturnPayment']!='' else None
                                        transportTypeWentID = int(data['TransportTypeWentID']) if data['TransportTypeWentID']!='' else None
                                        transportTypeReturnID = float(data['TransportTypeReturnID']) if data['TransportTypeReturnID']!='' else None
                                        Missions(UserID = int(session.get("user_id")), MissionTitle = str(data['MissionTitle']), StartDate = datetime.strptime(data['StartDate'], '%Y-%m-%d %H:%M'), EndDate = datetime.strptime(data['EndDate'], '%Y-%m-%d %H:%M'), Latitude = latitude, Longitude = longitude, TransportTypeWentID = transportTypeWentID, WentPayment = wentPayment, TransportTypeReturnID = transportTypeReturnID, ReturnPayment = returnPayment,  LatestUpdateDate = datetime.now())
                                        message = "Success"
                                        return jsonify({'message': message})
                        else:
                                return redirect("/AccessDenied", code=302)
                else:
                        return redirect("/", code=302)
        except Exception as e:
                message = str(e)
                return jsonify({'message': message})


@App.app.route('/MissionManagement/GetMission', methods=['GET', 'POST'])
@cross_origin(supports_credentials=True)
def GetMission():
        if session.get("user_id") is not None and session.get("fullname") is not None:
                if CheckAccess("Intra City Mission", "Read"):
                        with db_session:
                                data = request.get_json()
                                print(data['MissionID'])
                                query= Missions.select(lambda m: m.MissionID == int(data['MissionID']))
                                mylist = list(query)
                                transportTypeWentID = mylist[0].TransportTypeWentID.TransportTypeID if mylist[0].TransportTypeWentID is not None else ''
                                transportTypeWentTitle = mylist[0].TransportTypeWentID.TransportTypeTitle if mylist[0].TransportTypeWentID is not None else ''
                                transportTypeReturnID = mylist[0].TransportTypeReturnID.TransportTypeID if mylist[0].TransportTypeReturnID is not None else ''
                                transportTypeReturnTitle = mylist[0].TransportTypeReturnID.TransportTypeTitle if mylist[0].TransportTypeReturnID is not None else ''
                                approvalID = mylist[0].ApprovedBy.UserID if mylist[0].ApprovedBy is not None else ''
                                approvalName = mylist[0].ApprovedBy.FirstName+' '+mylist[0].ApprovedBy.LastName if mylist[0].ApprovedBy is not None else ''
                                return jsonify({'MissionID': mylist[0].MissionID, 'UserID': mylist[0].UserID.UserID, 'UserName': mylist[0].UserID.FirstName+' '+mylist[0].UserID.LastName,'StartDate': mylist[0].StartDate.strftime('%Y-%m-%d'),'StartTime': mylist[0].StartDate.strftime('%H:%M'), 'EndDate': mylist[0].EndDate.strftime('%Y-%m-%d'),'EndTime': mylist[0].EndDate.strftime('%H:%M'), 'IsApproved': mylist[0].IsApproved, "ApprovedByID": approvalID, "ApprovedByName": approvalName, "ApproveDate": mylist[0].ApproveDate, "MissionTitle": mylist[0].MissionTitle, "Latitude": mylist[0].Latitude, "Longitude": mylist[0].Longitude, "TransportTypeWentID": transportTypeWentID, "TransportTypeWentTitle": transportTypeWentTitle, "TransportTypeReturnID": transportTypeReturnID, "TransportTypeReturnTitle": transportTypeReturnTitle, "WentPayment": mylist[0].WentPayment, "ReturnPayment": mylist[0].ReturnPayment})
                else:
                        return redirect("/AccessDenied", code=302)
        else:
                return redirect("/", code=302)


@App.app.route('/MissionManagement/DeleteMission', methods=['GET', 'POST'])
@cross_origin(supports_credentials=True)
def DeleteMission():
        try:
                if session.get("user_id") is not None and session.get("fullname") is not None:
                        if CheckAccess("Intra City Mission", "Delete"):
                                with db_session:
                                        data = request.get_json()
                                        print(int(data["MissionID"]))
                                        query = list(Missions.select(lambda m: m.MissionID == int(data['MissionID'])))
                                        message = ""
                                        if int(query[0].UserID.UserID) ==  int(session.get("user_id")):
                                                if query[0].ApprovedBy is None:
                                                        delete(m for m in Missions if m.MissionID == int(data["MissionID"]))
                                                        message = "Success"
                                                else:
                                                        message = "Approval is submitted on this mission."
                                        else:
                                                message = "This mission is not related to logged in user."
                                        return jsonify({'message': message})
                        else:
                                return redirect("/AccessDenied", code=302)
                else:
                        return redirect("/", code=302)
        except Exception as e:
                message = str(e)
                return jsonify({'message': message})

@App.app.route('/MissionManagement/EditMission', methods=['GET', 'POST'])
@cross_origin(supports_credentials=True)
def EditMission():
        try:
                if session.get("user_id") is not None and session.get("fullname") is not None:
                        if CheckAccess("Intra City Mission", "Update"):
                                with db_session:
                                        data = request.get_json()
                                        query = list(Missions.select(lambda m: m.MissionID == int(data['MissionID'])))
                                        message = ""
                                        if int(query[0].UserID.UserID) ==  int(session.get("user_id")):
                                                if query[0].ApprovedBy is None:
                                                        latitude = float(data['Latitude']) if data['Latitude']!='' else None
                                                        longitude = float(data['Longitude']) if data['Longitude']!='' else None
                                                        wentPayment = float(data['WentPayment']) if data['WentPayment']!='' else None
                                                        returnPayment = float(data['ReturnPayment']) if data['ReturnPayment']!='' else None
                                                        transportTypeWentID = int(data['TransportTypeWentID']) if data['TransportTypeWentID']!='' else None
                                                        transportTypeReturnID = float(data['TransportTypeReturnID']) if data['TransportTypeReturnID']!='' else None
                                                        mission = Missions[int(data['MissionID'])]
                                                        mission.set(MissionTitle = str(data['MissionTitle']), StartDate = datetime.strptime(data['StartDate'], '%Y-%m-%d %H:%M'), EndDate = datetime.strptime(data['EndDate'], '%Y-%m-%d %H:%M'), Latitude = latitude, Longitude = longitude, TransportTypeWentID = transportTypeWentID, WentPayment = wentPayment, TransportTypeReturnID = transportTypeReturnID, ReturnPayment = returnPayment,  LatestUpdateDate = datetime.now())
                                                        message = "Success"
                                                else:
                                                        message = "Approval is submitted on this mission."
                                        else:
                                                message = "This mission is not related to logged in user."
                                        return jsonify({'message': message})
                        else:
                                return redirect("/AccessDenied", code=302)
                else:
                        return redirect("/", code=302)
        except Exception as e:
                message = str(e)
                return jsonify({'message': message})