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
from io import BytesIO, StringIO
import pandas as pd
import numpy as np
import csv
from werkzeug.datastructures import Headers
from werkzeug.wrappers import Response
from PollyReports import *
from reportlab.pdfgen.canvas import Canvas
from collections import namedtuple

@App.app.route('/MissionManagement/Missions')
def mission_page():
        if session.get("user_id") is not None and session.get("fullname") is not None:
                if CheckAccess("Intra City Mission", "Read"):
                        with db_session:
                                hometownarea = np.loadtxt('config/hometownarea.txt', dtype=np.object)
                                config = configparser.ConfigParser()
                                config.sections()
                                config.read('config/conf.ini')
                                search = False
                                page = request.args.get(get_page_parameter(), type=int, default=1)
                                mymissions = Missions.select(lambda l: l.UserID.UserID == int(session.get("user_id")) and l.IsIntraCityMission == True)
                                transporttypes = TransportTypes.select()
                                pagination = Pagination(page=page, total=mymissions.count(), search=search, record_name='intra city missions', css_framework='bootstrap4')
                                return render_template('MissionManagement/missions.html', mymissions = mymissions.page(page, 10), pagination = pagination, transporttypes = transporttypes, orglat = config['OrganizationInfo']['latitude'], orglong = config['OrganizationInfo']['longitude'], hometown = hometownarea.tolist(), formAccess = GetFormAccessControl("Intra City Mission"))
                else:
                        return redirect("/AccessDenied", code=302)
        else:
                return redirect("/", code=302)

@App.app.route('/MissionManagement/OutOfCityMission')
def out_of_city_mission_page():
        if session.get("user_id") is not None and session.get("fullname") is not None:
                if CheckAccess("Out of City Mission", "Read"):
                        with db_session:
                                hometownarea = np.loadtxt('config/hometownarea.txt', dtype=np.object)
                                config = configparser.ConfigParser()
                                config.sections()
                                config.read('config/conf.ini')
                                search = False
                                page = request.args.get(get_page_parameter(), type=int, default=1)
                                mymissions = Missions.select(lambda l: l.UserID.UserID == int(session.get("user_id")) and l.IsIntraCityMission == False)
                                transporttypes = TransportTypes.select()
                                pagination = Pagination(page=page, total=mymissions.count(), search=search, record_name='out of city missions', css_framework='bootstrap4')
                                return render_template('MissionManagement/outofcitymissions.html', mymissions = mymissions.page(page, 10), pagination = pagination, transporttypes = transporttypes, orglat = config['OrganizationInfo']['latitude'], orglong = config['OrganizationInfo']['longitude'], hometown = hometownarea.tolist(), formAccess = GetFormAccessControl("Out of City Mission"))
                else:
                        return redirect("/AccessDenied", code=302)
        else:
                return redirect("/", code=302)


@App.app.route('/MissionManagement/MissionApproval')
def mission_approval_page():
        if session.get("user_id") is not None and session.get("fullname") is not None:
                if CheckAccess("Mission Approval", "Read"):
                        with db_session:
                                hometownarea = np.loadtxt('config/hometownarea.txt', dtype=np.object)
                                config = configparser.ConfigParser()
                                config.sections()
                                config.read('config/conf.ini')
                                mymissions = Missions.select(lambda l: l.UserID.ManagerID.UserID == int(session.get("user_id")) and l.ApprovedBy is None)
                                return render_template('MissionManagement/missionapproval.html', mymissions = mymissions, orglat = config['OrganizationInfo']['latitude'], orglong = config['OrganizationInfo']['longitude'], hometown = hometownarea.tolist(), formAccess = GetFormAccessControl("Intra City Mission"))
                else:
                        return redirect("/AccessDenied", code=302)
        else:
                return redirect("/", code=302)

@App.app.route('/MissionManagement/ApproveMissions', methods=['Get','POST'])
def approve_missions_page():
        try:
                if session.get("user_id") is not None and session.get("fullname") is not None:
                        if CheckAccess("Mission Approval", "Update"):
                                with db_session:
                                        missions = request.form.getlist('missions')
                                        print(missions)
                                        isApproved = False
                                        if request.form['submit_approval'] == 'Approve':
                                                isApproved=True
                                        elif request.form['submit_approval'] == 'Reject':
                                                isApproved=False
                                        for m in missions:
                                                mission = Missions[int(m)]
                                                mission.set(ApprovedBy = int(session.get("user_id")), IsApproved = isApproved, ApproveDate = datetime.now(), LatestUpdateDate = datetime.now())
                                        commit()
                                        j = json.dumps(missions)
                                        InsertInfoLog('update', 'mission approval', None, j, None)
                                        return redirect("/MissionManagement/MissionApproval")
                        else:
                                return redirect("/AccessDenied", code=302)
                else:
                        return redirect("/", code=302)
        except Exception as e:
                InsertErrorLog('mission approval', 'update')
                message = str(e)
                return jsonify({'message': message})

@App.app.route('/MissionManagement/CreateMission', methods=['GET', 'POST'])
@cross_origin(supports_credentials=True)
def CreateMission():
        try:
                if session.get("user_id") is not None and session.get("fullname") is not None:
                        if CheckAccess("Intra City Mission", "Create"):
                                with db_session:
                                        with db.set_perms_for(Missions):
                                                perm('edit create delete view', group='anybody')
                                                data = request.get_json()
                                                latitude = float(data['Latitude']) if data['Latitude']!='' else None
                                                longitude = float(data['Longitude']) if data['Longitude']!='' else None
                                                wentPayment = float(data['WentPayment']) if data['WentPayment']!='' else None
                                                returnPayment = float(data['ReturnPayment']) if data['ReturnPayment']!='' else None
                                                transportTypeWentID = int(data['TransportTypeWentID']) if data['TransportTypeWentID']!='' else None
                                                transportTypeReturnID = float(data['TransportTypeReturnID']) if data['TransportTypeReturnID']!='' else None
                                                isIntraCityMission = bool(data['IsIntraCityMission'])
                                                mission = Missions(UserID = int(session.get("user_id")), MissionTitle = str(data['MissionTitle']), StartDate = datetime.strptime(data['StartDate'], '%Y-%m-%d %H:%M'), EndDate = datetime.strptime(data['EndDate'], '%Y-%m-%d %H:%M'), Latitude = latitude, Longitude = longitude, TransportTypeWentID = transportTypeWentID, WentPayment = wentPayment, TransportTypeReturnID = transportTypeReturnID, ReturnPayment = returnPayment,  LatestUpdateDate = datetime.now(), IsIntraCityMission = isIntraCityMission)
                                                commit()
                                                message = "Success"
                                                j = json.loads(mission.to_json())
                                                InsertInfoLog('create', 'mission', 'Missions', j,str(mission.MissionID))
                                                return jsonify({'message': message})
                        else:
                                return redirect("/AccessDenied", code=302)
                else:
                        return redirect("/", code=302)
        except Exception as e:
                InsertErrorLog('mission', 'create')
                message = str(e)
                return jsonify({'message': message})


@App.app.route('/MissionManagement/GetMission', methods=['GET', 'POST'])
@cross_origin(supports_credentials=True)
def GetMission():
        if session.get("user_id") is not None and session.get("fullname") is not None:
                if CheckAccess("Intra City Mission", "Read"):
                        with db_session:
                                data = request.get_json()
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
                                        with db.set_perms_for(Missions):
                                                perm('edit create delete view', group='anybody')
                                                data = request.get_json()
                                                print(int(data["MissionID"]))
                                                query = Missions.select(lambda m: m.MissionID == int(data['MissionID']))
                                                j = json.loads(query.to_json())
                                                query = list(query)
                                                message = ""
                                                if int(query[0].UserID.UserID) ==  int(session.get("user_id")):
                                                        if query[0].ApprovedBy is None:
                                                                delete(m for m in Missions if m.MissionID == int(data["MissionID"]))
                                                                commit()
                                                                message = "Success"
                                                                InsertInfoLog('delete', 'mission', 'Missions', j,str(data["MissionID"]))
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
                InsertErrorLog('mission', 'delete')
                message = str(e)
                return jsonify({'message': message})

@App.app.route('/MissionManagement/EditMission', methods=['GET', 'POST'])
@cross_origin(supports_credentials=True)
def EditMission():
        try:
                if session.get("user_id") is not None and session.get("fullname") is not None:
                        if CheckAccess("Intra City Mission", "Update"):
                                with db_session:
                                        with db.set_perms_for(Missions):
                                                perm('edit create delete view', group='anybody')
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
                                                                commit()
                                                                j = json.loads(mission.to_json())
                                                                message = "Success"
                                                                InsertInfoLog('update', 'mission', 'Missions', j,str(data["MissionID"]))
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
                InsertErrorLog('mission', 'update')
                message = str(e)
                return jsonify({'message': message})


@App.app.route('/MissionManagement/MissionExportReport', methods=['GET', 'POST'])
def MissionExportReport():
        if session.get("user_id") is not None and session.get("fullname") is not None:
                if CheckAccess("Intra City Mission", "Print"):
                        with db_session:
                                if request.form["reportType"] == 'Excel':
                                        output = BytesIO()
                                        writer = pd.ExcelWriter(output, engine='xlsxwriter')
                                        workbook = writer.book
                                        worksheet = workbook.add_worksheet()
                                        bold = workbook.add_format({'bold': True})
                                        date_format = workbook.add_format({'num_format': 'yyyy/mm/dd hh:mm'})
                                        worksheet.write('A1', 'No.', bold)
                                        worksheet.write('B1', 'Staff Name', bold)
                                        worksheet.write('C1', 'Start Date', bold)
                                        worksheet.write('D1', 'End Date', bold)
                                        worksheet.write('E1', 'Mission Title', bold)
                                        worksheet.write('F1', 'Approval Result', bold)
                                        worksheet.write('G1', 'Approved By', bold)
                                        worksheet.write('H1', 'Approve Date', bold)
                                        row = 1
                                        col = 0
                                        missions = Missions.select(lambda l: l.UserID.UserID == int(session.get("user_id")) and l.IsIntraCityMission == True)
                                        for item in missions:
                                                worksheet.write(row, col, row)
                                                worksheet.write(row, col + 1, item.UserID.FirstName+' '+item.UserID.LastName)
                                                worksheet.write(row, col + 2, item.StartDate, date_format)
                                                worksheet.write(row, col + 3, item.EndDate, date_format)
                                                worksheet.write(row, col + 4, item.MissionTitle)
                                                worksheet.write(row, col + 5, 'Approved' if item.IsApproved else 'Rejected' if item.IsApproved==False else 'Not Answered')
                                                worksheet.write(row, col + 6, item.ApprovedBy.FirstName+' '+item.ApprovedBy.LastName if item.ApprovedBy is not None else None)
                                                worksheet.write(row, col + 7, item.ApproveDate if item.ApproveDate is not None else None)
                                                row += 1
                                        writer.close()
                                        output.seek(0)
                                        return send_file(output, attachment_filename="IntraCityMissions-"+datetime.now().strftime("%Y%m%d%H%M%S")+".xlsx", as_attachment=True)
                                elif request.form["reportType"] == 'CVS':
                                        def generate():
                                                with db_session:
                                                        output = StringIO()
                                                        writer = csv.writer(output)
                                                        writer.writerow(('Staff Name', 'Start Date', 'End Date', 'Mission Title', 'Approve Result', 'Approved By', 'Approve Date'))
                                                        yield output.getvalue()
                                                        output.seek(0)
                                                        output.truncate(0)
                                                        missions = Missions.select(lambda l: l.UserID.UserID == int(session.get("user_id")) and l.IsIntraCityMission == True)
                                                        for item in missions:
                                                                writer.writerow((item.UserID.FirstName+' '+item.UserID.LastName,item.StartDate,item.EndDate,item.MissionTitle,'Approved' if item.IsApproved else 'Rejected' if item.IsApproved==False else 'Not Answered', item.ApprovedBy.FirstName+' '+item.ApprovedBy.LastName if item.ApprovedBy is not None else None, item.ApproveDate if item.ApproveDate is not None else None))
                                                                yield output.getvalue()
                                                                output.seek(0)
                                                                output.truncate(0)
                                        headers = Headers()
                                        headers.set('Content-Disposition', 'attachment', filename="IntraCityMissions-"+datetime.now().strftime("%Y%m%d%H%M%S")+".cvs")

                                        return Response(
                                                        stream_with_context(generate()),
                                                        mimetype='text/csv', headers=headers
                                        )
                                elif request.form["reportType"] == 'PDF':
                                        with db_session:
                                                with db.set_perms_for(Users):
                                                        currentDateTime = datetime.now()
                                                        perm('edit create delete view', group='anybody')
                                                        missions = namedtuple("Missions", "MissionID StaffName StartDate EndDate MissionTitle ApproveResult ApprovedBy ApproveDate")
                                                        missions = select(l for l in Missions if l.UserID.UserID == int(session.get("user_id")) and l.IsIntraCityMission == True)[:]
                                                        result = {'data': [{"MissionID": p.MissionID, "StaffName": p.UserID.FirstName+' '+p.UserID.LastName, "StartDate": p.StartDate, "EndDate": p.EndDate, "MissionTitle": p.MissionTitle, "ApproveResult": 'Approved' if p.IsApproved else 'Rejected' if p.IsApproved == False else 'Not Answered', "ApprovedBy":  p.ApprovedBy.FirstName+' '+p.ApprovedBy.LastName if p.ApprovedBy is not None else None, "ApproveDate": p.ApproveDate if p.ApproveDate is not None else None} for p in missions]}
                                                        rpt = Report(result["data"])
                                                        rpt.detailband = Band([
                                                                Element((36, 0), ("Helvetica", 9), key = "StaffName"),
                                                                Element((130, 0), ("Helvetica", 9), key = "StartDate"),
                                                                Element((230, 0), ("Helvetica", 9), key = "EndDate"),
                                                                Element((330, 0), ("Helvetica", 9), key = "MissionTitle"),
                                                                Element((430, 0), ("Helvetica", 9), key = "ApproveResult"),
                                                                Element((500, 0), ("Helvetica", 9), key = "ApprovedBy"),
                                                                Element((600, 0), ("Helvetica", 9), key = "ApproveDate"),
                                                        ])

                                                        rpt.pageheader = Band([
                                                                Element((36, 0), ("Helvetica-Bold", 20), text = "Staff's Intra City Missions List"),
                                                                Element((36, 30), ("Helvetica", 9), text = "Staff Name"),
                                                                Element((130, 30), ("Helvetica", 9), text = "Start Date"),
                                                                Element((230, 30), ("Helvetica", 9), text = "End Date"),
                                                                Element((330, 30), ("Helvetica", 9), text = "Mission Title"),
                                                                Element((430, 30), ("Helvetica", 9), text = "Approve Result"),
                                                                Element((500, 30), ("Helvetica", 9), text = "Approved By"),
                                                                Element((600, 30), ("Helvetica", 9), text = "Approve Date"),
                                                                Rule((36, 42), 9*72, thickness = 2),
                                                        ])

                                                        rpt.pagefooter = Band([
                                                                Element((72*9.5, 0), ("Helvetica-Bold", 14), text = currentDateTime.strftime("%Y/%m/%d %H:%M:%S"), align = "right"),
                                                                Element((36, 16), ("Helvetica-Bold", 12), sysvar = "pagenumber", format = lambda x: "Page %d" % x),
                                                        ])
                                                        
                                                        filename = "IntraCityMissions-"+currentDateTime.strftime("%Y%m%d%H%M%S")+".pdf"
                                                        output = BytesIO()
                                                        canvas = Canvas(output, (72*11, 72*8.5))
                                                        rpt.generate(canvas)
                                                        canvas.showPage()
                                                        canvas.save()
                                                        pdf_out = output.getvalue()
                                                        output.close()
                                                        response = make_response(pdf_out)
                                                        response.headers['Content-Disposition'] = "attachment; filename="+filename
                                                        response.mimetype = 'application/pdf'
                                                        return response
                else:
                        return redirect("/AccessDenied", code=302)
        else:
                return redirect("/", code=302)


@App.app.route('/MissionManagement/OutOfCityMissionExportReport', methods=['GET', 'POST'])
def OutOfCityMissionExportReport():
        if session.get("user_id") is not None and session.get("fullname") is not None:
                if CheckAccess("Out of City Mission", "Print"):
                        with db_session:
                                if request.form["reportType"] == 'Excel':
                                        output = BytesIO()
                                        writer = pd.ExcelWriter(output, engine='xlsxwriter')
                                        workbook = writer.book
                                        worksheet = workbook.add_worksheet()
                                        bold = workbook.add_format({'bold': True})
                                        date_format = workbook.add_format({'num_format': 'yyyy/mm/dd hh:mm'})
                                        worksheet.write('A1', 'No.', bold)
                                        worksheet.write('B1', 'Staff Name', bold)
                                        worksheet.write('C1', 'Start Date', bold)
                                        worksheet.write('D1', 'End Date', bold)
                                        worksheet.write('E1', 'Mission Title', bold)
                                        worksheet.write('F1', 'Approval Result', bold)
                                        worksheet.write('G1', 'Approved By', bold)
                                        worksheet.write('H1', 'Approve Date', bold)
                                        row = 1
                                        col = 0
                                        missions = Missions.select(lambda l: l.UserID.UserID == int(session.get("user_id")) and l.IsIntraCityMission == False)
                                        for item in missions:
                                                worksheet.write(row, col, row)
                                                worksheet.write(row, col + 1, item.UserID.FirstName+' '+item.UserID.LastName)
                                                worksheet.write(row, col + 2, item.StartDate, date_format)
                                                worksheet.write(row, col + 3, item.EndDate, date_format)
                                                worksheet.write(row, col + 4, item.MissionTitle)
                                                worksheet.write(row, col + 5, 'Approved' if item.IsApproved else 'Rejected' if item.IsApproved==False else 'Not Answered')
                                                worksheet.write(row, col + 6, item.ApprovedBy.FirstName+' '+item.ApprovedBy.LastName if item.ApprovedBy is not None else None)
                                                worksheet.write(row, col + 7, item.ApproveDate if item.ApproveDate is not None else None)
                                                row += 1
                                        writer.close()
                                        output.seek(0)
                                        return send_file(output, attachment_filename="OutOfCityMissions-"+datetime.now().strftime("%Y%m%d%H%M%S")+".xlsx", as_attachment=True)
                                elif request.form["reportType"] == 'CVS':
                                        def generate():
                                                with db_session:
                                                        output = StringIO()
                                                        writer = csv.writer(output)
                                                        writer.writerow(('Staff Name', 'Start Date', 'End Date', 'Mission Title', 'Approve Result', 'Approved By', 'Approve Date'))
                                                        yield output.getvalue()
                                                        output.seek(0)
                                                        output.truncate(0)
                                                        missions = Missions.select(lambda l: l.UserID.UserID == int(session.get("user_id")) and l.IsIntraCityMission == False)
                                                        for item in missions:
                                                                writer.writerow((item.UserID.FirstName+' '+item.UserID.LastName,item.StartDate,item.EndDate,item.MissionTitle,'Approved' if item.IsApproved else 'Rejected' if item.IsApproved==False else 'Not Answered', item.ApprovedBy.FirstName+' '+item.ApprovedBy.LastName if item.ApprovedBy is not None else None, item.ApproveDate if item.ApproveDate is not None else None))
                                                                yield output.getvalue()
                                                                output.seek(0)
                                                                output.truncate(0)
                                        headers = Headers()
                                        headers.set('Content-Disposition', 'attachment', filename="OutOfCityMissions-"+datetime.now().strftime("%Y%m%d%H%M%S")+".cvs")

                                        return Response(
                                                        stream_with_context(generate()),
                                                        mimetype='text/csv', headers=headers
                                        )
                                elif request.form["reportType"] == 'PDF':
                                        with db_session:
                                                with db.set_perms_for(Users):
                                                        currentDateTime = datetime.now()
                                                        perm('edit create delete view', group='anybody')
                                                        missions = namedtuple("Missions", "MissionID StaffName StartDate EndDate MissionTitle ApproveResult ApprovedBy ApproveDate")
                                                        missions = select(l for l in Missions if l.UserID.UserID == int(session.get("user_id")) and l.IsIntraCityMission == False)[:]
                                                        result = {'data': [{"MissionID": p.MissionID, "StaffName": p.UserID.FirstName+' '+p.UserID.LastName, "StartDate": p.StartDate, "EndDate": p.EndDate, "MissionTitle": p.MissionTitle, "ApproveResult": 'Approved' if p.IsApproved else 'Rejected' if p.IsApproved == False else 'Not Answered', "ApprovedBy":  p.ApprovedBy.FirstName+' '+p.ApprovedBy.LastName if p.ApprovedBy is not None else None, "ApproveDate": p.ApproveDate if p.ApproveDate is not None else None} for p in missions]}
                                                        rpt = Report(result["data"])
                                                        rpt.detailband = Band([
                                                                Element((36, 0), ("Helvetica", 9), key = "StaffName"),
                                                                Element((130, 0), ("Helvetica", 9), key = "StartDate"),
                                                                Element((230, 0), ("Helvetica", 9), key = "EndDate"),
                                                                Element((330, 0), ("Helvetica", 9), key = "MissionTitle"),
                                                                Element((430, 0), ("Helvetica", 9), key = "ApproveResult"),
                                                                Element((500, 0), ("Helvetica", 9), key = "ApprovedBy"),
                                                                Element((600, 0), ("Helvetica", 9), key = "ApproveDate"),
                                                        ])

                                                        rpt.pageheader = Band([
                                                                Element((36, 0), ("Helvetica-Bold", 20), text = "Staff's Intra City Missions List"),
                                                                Element((36, 30), ("Helvetica", 9), text = "Staff Name"),
                                                                Element((130, 30), ("Helvetica", 9), text = "Start Date"),
                                                                Element((230, 30), ("Helvetica", 9), text = "End Date"),
                                                                Element((330, 30), ("Helvetica", 9), text = "Mission Title"),
                                                                Element((430, 30), ("Helvetica", 9), text = "Approve Result"),
                                                                Element((500, 30), ("Helvetica", 9), text = "Approved By"),
                                                                Element((600, 30), ("Helvetica", 9), text = "Approve Date"),
                                                                Rule((36, 42), 9*72, thickness = 2),
                                                        ])

                                                        rpt.pagefooter = Band([
                                                                Element((72*9.5, 0), ("Helvetica-Bold", 14), text = currentDateTime.strftime("%Y/%m/%d %H:%M:%S"), align = "right"),
                                                                Element((36, 16), ("Helvetica-Bold", 12), sysvar = "pagenumber", format = lambda x: "Page %d" % x),
                                                        ])
                                                        
                                                        filename = "OutOfCityMissions-"+currentDateTime.strftime("%Y%m%d%H%M%S")+".pdf"
                                                        output = BytesIO()
                                                        canvas = Canvas(output, (72*11, 72*8.5))
                                                        rpt.generate(canvas)
                                                        canvas.showPage()
                                                        canvas.save()
                                                        pdf_out = output.getvalue()
                                                        output.close()
                                                        response = make_response(pdf_out)
                                                        response.headers['Content-Disposition'] = "attachment; filename="+filename
                                                        response.mimetype = 'application/pdf'
                                                        return response
                else:
                        return redirect("/AccessDenied", code=302)
        else:
                return redirect("/", code=302)