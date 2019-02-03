import sys
import random, json
from pony import orm
from flask import *
from flask_cors import *
import App
from models.DatabaseContext import *
import hashlib
from datetime import datetime

@App.app.route('/LeaveManagement/Leaves')
def leave_page():
    if session.get("user_id") is not None and session.get("fullname") is not None:
        with db_session:
            myleaves = Leaves.select(lambda l: l.UserID.UserID == int(session.get("user_id")))
            return render_template('LeaveManagement/Leaves.html', myleaves = myleaves)
    else:
        return redirect("/", code=302)

@App.app.route('/LeaveManagement/CreateLeave', methods=['GET', 'POST'])
@cross_origin(supports_credentials=True)
def CreateLeave():
        try:
                if session.get("user_id") is not None and session.get("fullname") is not None:
                        with db_session:
                                data = request.get_json()
                                print(data['StartDate'])
                                print(data['EndDate'])
                                print(session.get("user_id"))
                                Leaves(UserID = int(session.get("user_id")), StartDate = datetime.strptime(data['StartDate'], '%Y-%m-%d %H:%M'), EndDate = datetime.strptime(data['EndDate'], '%Y-%m-%d %H:%M'), Reason = str(data['Reason']), LatestUpdateDate = datetime.now())
                                message = "Success"
                                return jsonify({'message': message})
                else:
                        return redirect("/", code=302)
        except Exception as e:
                message = str(e)
                return jsonify({'message': message})


@App.app.route('/LeaveManagement/GetLeave', methods=['GET', 'POST'])
@cross_origin(supports_credentials=True)
def GetLeave():
    if session.get("user_id") is not None and session.get("fullname") is not None:
        with db_session:
            data = request.get_json()
            query= Leaves.select(lambda u: u.LeaveID == int(data['LeaveID']))
            mylist = list(query)
            approvalID = mylist[0].ApprovedBy.UserID if mylist[0].ApprovedBy is not None else ''
            approvalName = mylist[0].ApprovedBy.FirstName+' '+mylist[0].ApprovedBy.LastName if mylist[0].ApprovedBy is not None else ''
            return jsonify({'LeaveID': mylist[0].LeaveID, 'UserID': mylist[0].UserID.UserID, 'UserName': mylist[0].UserID.FirstName+' '+mylist[0].UserID.LastName,'StartDate': mylist[0].StartDate.strftime('%Y-%m-%d'),'StartTime': mylist[0].StartDate.strftime('%H:%M'), 'EndDate': mylist[0].EndDate.strftime('%Y-%m-%d'),'EndTime': mylist[0].EndDate.strftime('%H:%M'), 'IsApproved': mylist[0].IsApproved, "ApprovedByID": approvalID, "ApprovedByName": approvalName, "ApproveDate": mylist[0].ApproveDate, "Reason": mylist[0].Reason})
    else:
        return redirect("/", code=302)


@App.app.route('/LeaveManagement/DeleteLeave', methods=['GET', 'POST'])
@cross_origin(supports_credentials=True)
def DeleteLeave():
        try:
                if session.get("user_id") is not None and session.get("fullname") is not None:
                        with db_session:
                                data = request.get_json()
                                print(int(data["LeaveID"]))
                                query = list(Leaves.select(lambda u: u.LeaveID == int(data['LeaveID'])))
                                message = ""
                                if int(query[0].UserID.UserID) ==  int(session.get("user_id")):
                                    if query[0].ApprovedBy is None:
                                        delete(l for l in Leaves if l.LeaveID == int(data["LeaveID"]))
                                        message = "Success"
                                    else:
                                        message = "Approval is submitted on this leave."
                                else:
                                    message = "This leave is not related to logged in user."
                                return jsonify({'message': message})
                else:
                        return redirect("/", code=302)
        except Exception as e:
                message = str(e)
                return jsonify({'message': message})

@App.app.route('/LeaveManagement/EditLeave', methods=['GET', 'POST'])
@cross_origin(supports_credentials=True)
def EditLeave():
        try:
                if session.get("user_id") is not None and session.get("fullname") is not None:
                        with db_session:
                                data = request.get_json()
                                query = list(Leaves.select(lambda u: u.LeaveID == int(data['LeaveID'])))
                                message = ""
                                if int(query[0].UserID.UserID) ==  int(session.get("user_id")):
                                    if query[0].ApprovedBy is None:
                                        leave = Leaves[int(data['LeaveID'])]
                                        leave.set(StartDate = datetime.strptime(data['StartDate'], '%Y-%m-%d %H:%M'), EndDate = datetime.strptime(data['EndDate'], '%Y-%m-%d %H:%M'), Reason = data['Reason'], LatestUpdateDate = datetime.now())
                                        message = "Success"
                                    else:
                                        message = "Approval is submitted on this leave."
                                else:
                                    message = "This leave is not related to logged in user."
                                return jsonify({'message': message})
                else:
                        return redirect("/", code=302)
        except Exception as e:
                message = str(e)
                return jsonify({'message': message})