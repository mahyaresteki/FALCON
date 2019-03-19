import sys
import random, json
from pony import orm
from flask import *
from flask_cors import *
from flask_paginate import Pagination, get_page_parameter
import App
from models.DatabaseContext import *
import hashlib
from datetime import datetime
from controllers.Security import CheckAccess, GetFormAccessControl
from ConfigLogging import *

@App.app.route('/LeaveManagement/Leaves')
def leave_page():
        if session.get("user_id") is not None and session.get("fullname") is not None:
                if CheckAccess("Leaves", "Read"):
                        with db_session:
                                search = False
                                page = request.args.get(get_page_parameter(), type=int, default=1)
                                myleaves = Leaves.select(lambda l: l.UserID.UserID == int(session.get("user_id")) and l.StartDate.date() < l.EndDate.date())
                                pagination = Pagination(page=page, total=myleaves.count(), search=search, record_name='leaves', css_framework='bootstrap4')
                                return render_template('LeaveManagement/Leaves.html', myleaves = myleaves.page(page, 10), pagination = pagination, formAccess = GetFormAccessControl("Leaves"))
                else:
                        return redirect("/AccessDenied", code=302)
        else:
                return redirect("/", code=302)

@App.app.route('/LeaveManagement/HourOff')
def houroff_page():
        if session.get("user_id") is not None and session.get("fullname") is not None:
                if CheckAccess("Hour Off Leave", "Read"):
                        with db_session:
                                search = False
                                page = request.args.get(get_page_parameter(), type=int, default=1)
                                myleaves = Leaves.select(lambda l: l.UserID.UserID == int(session.get("user_id") and l.StartDate.date() == l.EndDate.date()))
                                pagination = Pagination(page=page, total=myleaves.count(), search=search, record_name='hour off leaves', css_framework='bootstrap4')
                                return render_template('LeaveManagement/houroff.html', myleaves = myleaves.page(page, 10), pagination = pagination, formAccess = GetFormAccessControl("Hour Off Leave"))
                else:
                        return redirect("/AccessDenied", code=302)
        else:
                return redirect("/", code=302)

@App.app.route('/LeaveManagement/CreateLeave', methods=['GET', 'POST'])
@cross_origin(supports_credentials=True)
def CreateLeave():
        try:
                if session.get("user_id") is not None and session.get("fullname") is not None:
                        if CheckAccess("Leaves", "Create"):
                                with db_session:
                                        with db.set_perms_for(Leaves):
                                                perm('edit create delete view', group='anybody')
                                                data = request.get_json()
                                                leave = Leaves(UserID = int(session.get("user_id")), StartDate = datetime.strptime(data['StartDate'], '%Y-%m-%d %H:%M'), EndDate = datetime.strptime(data['EndDate'], '%Y-%m-%d %H:%M'), Reason = str(data['Reason']), LatestUpdateDate = datetime.now())
                                                commit()
                                                message = "Success"
                                                j = json.loads(leave.to_json())
                                                InsertInfoLog('create', 'leave', 'Leaves', j,str(data["LeaveID"]))
                                                return jsonify({'message': message})
                        else:
                                return redirect("/AccessDenied", code=302)
                else:
                        return redirect("/", code=302)
        except Exception as e:
                InsertErrorLog('leave', 'create')
                message = str(e)
                return jsonify({'message': message})


@App.app.route('/LeaveManagement/GetLeave', methods=['GET', 'POST'])
@cross_origin(supports_credentials=True)
def GetLeave():
        if session.get("user_id") is not None and session.get("fullname") is not None:
                if CheckAccess("Leaves", "Read"):
                        with db_session:
                                with db.set_perms_for(Leaves):
                                        perm('edit create delete view', group='anybody')
                                        data = request.get_json()
                                        query= Leaves.select(lambda u: u.LeaveID == int(data['LeaveID']))
                                        mylist = list(query)
                                        approvalID = mylist[0].ApprovedBy.UserID if mylist[0].ApprovedBy is not None else ''
                                        approvalName = mylist[0].ApprovedBy.FirstName+' '+mylist[0].ApprovedBy.LastName if mylist[0].ApprovedBy is not None else ''
                                        return jsonify({'LeaveID': mylist[0].LeaveID, 'UserID': mylist[0].UserID.UserID, 'UserName': mylist[0].UserID.FirstName+' '+mylist[0].UserID.LastName,'StartDate': mylist[0].StartDate.strftime('%Y-%m-%d'),'StartTime': mylist[0].StartDate.strftime('%H:%M'), 'EndDate': mylist[0].EndDate.strftime('%Y-%m-%d'),'EndTime': mylist[0].EndDate.strftime('%H:%M'), 'IsApproved': mylist[0].IsApproved, "ApprovedByID": approvalID, "ApprovedByName": approvalName, "ApproveDate": mylist[0].ApproveDate, "Reason": mylist[0].Reason})
                else:
                        return redirect("/AccessDenied", code=302)
        else:
                return redirect("/", code=302)


@App.app.route('/LeaveManagement/DeleteLeave', methods=['GET', 'POST'])
@cross_origin(supports_credentials=True)
def DeleteLeave():
        try:
                if session.get("user_id") is not None and session.get("fullname") is not None:
                        if CheckAccess("Leaves", "Delete"):
                                with db_session:
                                        with db.set_perms_for(Leaves):
                                                perm('edit create delete view', group='anybody')
                                                data = request.get_json()
                                                print(int(data["LeaveID"]))
                                                query = list(Leaves.select(lambda u: u.LeaveID == int(data['LeaveID'])))
                                                j = json.loads(query.to_json())
                                                message = ""
                                                if int(query[0].UserID.UserID) ==  int(session.get("user_id")):
                                                        if query[0].ApprovedBy is None:
                                                                delete(l for l in Leaves if l.LeaveID == int(data["LeaveID"]))
                                                                commit()
                                                                message = "Success"
                                                                InsertInfoLog('delete', 'leave', 'Leaves', j,str(data["LeaveID"]))
                                                        else:
                                                                message = "Approval is submitted on this leave."
                                                else:
                                                        message = "This leave is not related to logged in user."
                                                return jsonify({'message': message})
                        else:
                                return redirect("/AccessDenied", code=302)
                else:
                        return redirect("/", code=302)
        except Exception as e:
                InsertErrorLog('leave', 'delete')
                message = str(e)
                return jsonify({'message': message})

@App.app.route('/LeaveManagement/EditLeave', methods=['GET', 'POST'])
@cross_origin(supports_credentials=True)
def EditLeave():
        try:
                if session.get("user_id") is not None and session.get("fullname") is not None:
                        if CheckAccess("Leaves", "Update"):
                                with db_session:
                                        with db.set_perms_for(Leaves):
                                                perm('edit create delete view', group='anybody')
                                                data = request.get_json()
                                                query = list(Leaves.select(lambda u: u.LeaveID == int(data['LeaveID'])))
                                                message = ""
                                                if int(query[0].UserID.UserID) ==  int(session.get("user_id")):
                                                        if query[0].ApprovedBy is None:
                                                                leave = Leaves[int(data['LeaveID'])]
                                                                leave.set(StartDate = datetime.strptime(data['StartDate'], '%Y-%m-%d %H:%M'), EndDate = datetime.strptime(data['EndDate'], '%Y-%m-%d %H:%M'), Reason = data['Reason'], LatestUpdateDate = datetime.now())
                                                                commit()
                                                                message = "Success"
                                                                j = json.loads(leave.to_json())
                                                                InsertInfoLog('update', 'leave', 'Leaves', j,str(data["LeaveID"]))
                                                        else:
                                                                message = "Approval is submitted on this leave."
                                                else:
                                                        message = "This leave is not related to logged in user."
                                                return jsonify({'message': message})
                        else:
                                return redirect("/AccessDenied", code=302)
                else:
                        return redirect("/", code=302)
        except Exception as e:
                InsertErrorLog('leave', 'update')
                message = str(e)
                return jsonify({'message': message})