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

@App.app.route('/LeaveManagement/Leaves')
def leave_page():
        if session.get("user_id") is not None and session.get("fullname") is not None:
                if CheckAccess("Leaves", "Read"):
                        with db_session:
                                search = False
                                page = request.args.get(get_page_parameter(), type=int, default=1)
                                myleaves = Leaves.select(lambda l: l.UserID.UserID == int(session.get("user_id")) and l.StartDate.date() < l.EndDate.date())
                                pagination = Pagination(page=page, total=myleaves.count(), search=search, record_name='leaves', css_framework='bootstrap4')
                                leaveTypes = LeaveTypes.select()
                                return render_template('LeaveManagement/leaves.html', myleaves = myleaves.page(page, 10), pagination = pagination, formAccess = GetFormAccessControl("Leaves"), leaveTypes = leaveTypes)
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
                                leaveTypes = LeaveTypes.select()
                                return render_template('LeaveManagement/houroff.html', myleaves = myleaves.page(page, 10), pagination = pagination, formAccess = GetFormAccessControl("Hour Off Leave"), leaveTypes = leaveTypes)
                else:
                        return redirect("/AccessDenied", code=302)
        else:
                return redirect("/", code=302)

@App.app.route('/LeaveManagement/LeaveApproval')
def leave_approval_page():
        if session.get("user_id") is not None and session.get("fullname") is not None:
                if CheckAccess("Leave Approval", "Read"):
                        with db_session:
                                myleaves = Leaves.select(lambda l: l.UserID.ManagerID.UserID == int(session.get("user_id")) and l.ApprovedBy is None)
                                return render_template('LeaveManagement/leaveapproval.html', myleaves = myleaves, formAccess = GetFormAccessControl("Leave Approval"))
                else:
                        return redirect("/AccessDenied", code=302)
        else:
                return redirect("/", code=302)

@App.app.route('/LeaveManagement/ApproveLeaves', methods=['Get','POST'])
def approve_leaves_page():
        try:
                if session.get("user_id") is not None and session.get("fullname") is not None:
                        if CheckAccess("Leave Approval", "Update"):
                                with db_session:
                                        leaves = request.form.getlist('leaves')
                                        isApproved = False
                                        if request.form['submit_approval'] == 'Approve':
                                                isApproved=True
                                        elif request.form['submit_approval'] == 'Reject':
                                                isApproved=False
                                        for l in leaves:
                                                leave = Leaves[int(l)]
                                                leave.set(ApprovedBy = int(session.get("user_id")), IsApproved = isApproved, ApproveDate = datetime.now(), LatestUpdateDate = datetime.now())
                                        commit()
                                        j = json.dumps(leaves)
                                        InsertInfoLog('update', 'leave approval', None, j, None)
                                        return redirect("/LeaveManagement/LeaveApproval")
                        else:
                                return redirect("/AccessDenied", code=302)
                else:
                        return redirect("/", code=302)
        except Exception as e:
                InsertErrorLog('leave approval', 'update')
                message = str(e)
                return jsonify({'message': message})

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
                                                leave = Leaves(UserID = int(session.get("user_id")), StartDate = datetime.strptime(data['StartDate'], '%Y-%m-%d %H:%M'), EndDate = datetime.strptime(data['EndDate'], '%Y-%m-%d %H:%M'), Reason = str(data['Reason']), LeaveTypeID = int(data['LeaveTypeID']), LatestUpdateDate = datetime.now())
                                                commit()
                                                message = "Success"
                                                j = json.loads(leave.to_json())
                                                InsertInfoLog('create', 'leave', 'Leaves', j,str(leave.LeaveID))
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
                                        return jsonify({'LeaveID': mylist[0].LeaveID, 'UserID': mylist[0].UserID.UserID, 'UserName': mylist[0].UserID.FirstName+' '+mylist[0].UserID.LastName,'StartDate': mylist[0].StartDate.strftime('%Y-%m-%d'),'StartTime': mylist[0].StartDate.strftime('%H:%M'), 'EndDate': mylist[0].EndDate.strftime('%Y-%m-%d'),'EndTime': mylist[0].EndDate.strftime('%H:%M'), 'IsApproved': mylist[0].IsApproved, "ApprovedByID": approvalID, "ApprovedByName": approvalName, "ApproveDate": mylist[0].ApproveDate, "Reason": mylist[0].Reason, "LeaveTypeTitle": mylist[0].LeaveTypeID.LeaveTypeTitle})
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
                                                query = Leaves.select(lambda u: u.LeaveID == int(data['LeaveID']))
                                                j = json.loads(query.to_json())
                                                query = list(query)
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
                                                                leave.set(StartDate = datetime.strptime(data['StartDate'], '%Y-%m-%d %H:%M'), EndDate = datetime.strptime(data['EndDate'], '%Y-%m-%d %H:%M'), Reason = data['Reason'], LeaveTypeID = int(data['LeaveTypeID']), LatestUpdateDate = datetime.now())
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

@App.app.route('/LeaveManagement/LeaveExportReport', methods=['GET', 'POST'])
def LeaveExportReport():
        if session.get("user_id") is not None and session.get("fullname") is not None:
                if CheckAccess("Leaves", "Print"):
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
                                        worksheet.write('E1', 'Reason', bold)
                                        worksheet.write('F1', 'Leave Type', bold)
                                        worksheet.write('G1', 'Approval Result', bold)
                                        worksheet.write('H1', 'Approved By', bold)
                                        worksheet.write('I1', 'Approve Date', bold)
                                        row = 1
                                        col = 0
                                        leaves = Leaves.select(lambda l: l.UserID.UserID == int(session.get("user_id")) and l.StartDate.date() < l.EndDate.date())
                                        for item in leaves:
                                                worksheet.write(row, col, row)
                                                worksheet.write(row, col + 1, item.UserID.FirstName+' '+item.UserID.LastName)
                                                worksheet.write(row, col + 2, item.StartDate, date_format)
                                                worksheet.write(row, col + 3, item.EndDate, date_format)
                                                worksheet.write(row, col + 4, item.Reason)
                                                worksheet.write(row, col + 5, item.LeaveTypeID.LeaveTypeTitle)
                                                worksheet.write(row, col + 6, 'Approved' if item.IsApproved else 'Rejected' if item.IsApproved==False else 'Not Answered')
                                                worksheet.write(row, col + 7, item.ApprovedBy.FirstName+' '+item.ApprovedBy.LastName if item.ApprovedBy is not None else None)
                                                worksheet.write(row, col + 8, item.ApproveDate if item.ApproveDate is not None else None)
                                                row += 1
                                        writer.close()
                                        output.seek(0)
                                        return send_file(output, attachment_filename="Leaves-"+datetime.now().strftime("%Y%m%d%H%M%S")+".xlsx", as_attachment=True)
                                elif request.form["reportType"] == 'CVS':
                                        def generate():
                                                with db_session:
                                                        output = StringIO()
                                                        writer = csv.writer(output)
                                                        writer.writerow(('Staff Name', 'Start Date', 'End Date', 'Reason', 'Leave Type', 'Approve Result', 'Approved By', 'Approve Date'))
                                                        yield output.getvalue()
                                                        output.seek(0)
                                                        output.truncate(0)
                                                        leaves = Leaves.select(lambda l: l.UserID.UserID == int(session.get("user_id")) and l.StartDate.date() < l.EndDate.date())
                                                        for item in leaves:
                                                                writer.writerow((item.UserID.FirstName+' '+item.UserID.LastName,item.StartDate,item.EndDate,item.Reason,item.LeaveTypeID.LeaveTypeTitle,'Approved' if item.IsApproved else 'Rejected' if item.IsApproved==False else 'Not Answered', item.ApprovedBy.FirstName+' '+item.ApprovedBy.LastName if item.ApprovedBy is not None else None, item.ApproveDate if item.ApproveDate is not None else None))
                                                                yield output.getvalue()
                                                                output.seek(0)
                                                                output.truncate(0)
                                        headers = Headers()
                                        headers.set('Content-Disposition', 'attachment', filename="Leaves-"+datetime.now().strftime("%Y%m%d%H%M%S")+".cvs")

                                        return Response(
                                                        stream_with_context(generate()),
                                                        mimetype='text/csv', headers=headers
                                        )
                                elif request.form["reportType"] == 'PDF':
                                        with db_session:
                                                with db.set_perms_for(Users):
                                                        currentDateTime = datetime.now()
                                                        perm('edit create delete view', group='anybody')
                                                        leaves = namedtuple("Leaves", "LeaveID StaffName StartDate EndDate Reason ApproveResult ApprovedBy ApproveDate")
                                                        leaves = select(l for l in Leaves if l.UserID.UserID == int(session.get("user_id")) and l.StartDate.date() < l.EndDate.date())[:]
                                                        result = {'data': [{"LeaveID": p.LeaveID, "StaffName": p.UserID.FirstName+' '+p.UserID.LastName, "StartDate": p.StartDate, "EndDate": p.EndDate, "Reason": p.Reason, "ApproveResult": 'Approved', "LeaveType": p.LeaveTypeID.LeaveTypeTitle if p.IsApproved else 'Rejected' if p.IsApproved == False else 'Not Answered', "ApprovedBy":  p.ApprovedBy.FirstName+' '+p.ApprovedBy.LastName if p.ApprovedBy is not None else None, "ApproveDate": p.ApproveDate if p.ApproveDate is not None else None} for p in leaves]}
                                                        rpt = Report(result["data"])
                                                        rpt.detailband = Band([
                                                                Element((36, 0), ("Helvetica", 9), key = "StaffName"),
                                                                Element((130, 0), ("Helvetica", 9), key = "StartDate"),
                                                                Element((230, 0), ("Helvetica", 9), key = "EndDate"),
                                                                Element((330, 0), ("Helvetica", 9), key = "Reason"),
                                                                Element((430, 0), ("Helvetica", 9), key = "LeaveType"),
                                                                Element((500, 0), ("Helvetica", 9), key = "ApproveResult"),
                                                                Element((600, 0), ("Helvetica", 9), key = "ApprovedBy"),
                                                                Element((700, 0), ("Helvetica", 9), key = "ApproveDate"),
                                                        ])

                                                        rpt.pageheader = Band([
                                                                Element((36, 0), ("Helvetica-Bold", 20), text = "Staff's Leave List"),
                                                                Element((36, 30), ("Helvetica", 9), text = "Staff Name"),
                                                                Element((130, 30), ("Helvetica", 9), text = "Start Date"),
                                                                Element((230, 30), ("Helvetica", 9), text = "End Date"),
                                                                Element((330, 30), ("Helvetica", 9), text = "Reason"),
                                                                Element((430, 30), ("Helvetica", 9), text = "Leave Type"),
                                                                Element((500, 30), ("Helvetica", 9), text = "Approve Result"),
                                                                Element((600, 30), ("Helvetica", 9), text = "Approved By"),
                                                                Element((700, 30), ("Helvetica", 9), text = "Approve Date"),
                                                                Rule((36, 42), 9*72, thickness = 2),
                                                        ])

                                                        rpt.pagefooter = Band([
                                                                Element((72*9.5, 0), ("Helvetica-Bold", 14), text = currentDateTime.strftime("%Y/%m/%d %H:%M:%S"), align = "right"),
                                                                Element((36, 16), ("Helvetica-Bold", 12), sysvar = "pagenumber", format = lambda x: "Page %d" % x),
                                                        ])
                                                        
                                                        filename = "Leaves-"+currentDateTime.strftime("%Y%m%d%H%M%S")+".pdf"
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



@App.app.route('/LeaveManagement/HourOffExportReport', methods=['GET', 'POST'])
def HourOffExportReport():
        if session.get("user_id") is not None and session.get("fullname") is not None:
                if CheckAccess("Hour Off Leave", "Print"):
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
                                        worksheet.write('E1', 'Reason', bold)
                                        worksheet.write('F1', 'Approval Result', bold)
                                        worksheet.write('G1', 'Approved By', bold)
                                        worksheet.write('H1', 'Approve Date', bold)
                                        row = 1
                                        col = 0
                                        leaves = Leaves.select(lambda l: l.UserID.UserID == int(session.get("user_id") and l.StartDate.date() == l.EndDate.date()))
                                        for item in leaves:
                                                worksheet.write(row, col, row)
                                                worksheet.write(row, col + 1, item.UserID.FirstName+' '+item.UserID.LastName)
                                                worksheet.write(row, col + 2, item.StartDate, date_format)
                                                worksheet.write(row, col + 3, item.EndDate, date_format)
                                                worksheet.write(row, col + 4, item.Reason)
                                                worksheet.write(row, col + 5, 'Approved' if item.IsApproved else 'Rejected' if item.IsApproved==False else 'Not Answered')
                                                worksheet.write(row, col + 6, item.ApprovedBy.FirstName+' '+item.ApprovedBy.LastName if item.ApprovedBy is not None else None)
                                                worksheet.write(row, col + 7, item.ApproveDate if item.ApproveDate is not None else None)
                                                row += 1
                                        writer.close()
                                        output.seek(0)
                                        return send_file(output, attachment_filename="HourOffLeaves-"+datetime.now().strftime("%Y%m%d%H%M%S")+".xlsx", as_attachment=True)
                                elif request.form["reportType"] == 'CVS':
                                        def generate():
                                                with db_session:
                                                        output = StringIO()
                                                        writer = csv.writer(output)
                                                        writer.writerow(('Staff Name', 'Start Date', 'End Date', 'Reason', 'Approve Result', 'Approved By', 'Approve Date'))
                                                        yield output.getvalue()
                                                        output.seek(0)
                                                        output.truncate(0)
                                                        leaves = Leaves.select(lambda l: l.UserID.UserID == int(session.get("user_id")) and l.StartDate.date() == l.EndDate.date())
                                                        for item in leaves:
                                                                writer.writerow((item.UserID.FirstName+' '+item.UserID.LastName,item.StartDate,item.EndDate,item.Reason,'Approved' if item.IsApproved else 'Rejected' if item.IsApproved==False else 'Not Answered', item.ApprovedBy.FirstName+' '+item.ApprovedBy.LastName if item.ApprovedBy is not None else None, item.ApproveDate if item.ApproveDate is not None else None))
                                                                yield output.getvalue()
                                                                output.seek(0)
                                                                output.truncate(0)
                                        headers = Headers()
                                        headers.set('Content-Disposition', 'attachment', filename="HourOffLeaves-"+datetime.now().strftime("%Y%m%d%H%M%S")+".cvs")

                                        return Response(
                                                        stream_with_context(generate()),
                                                        mimetype='text/csv', headers=headers
                                        )
                                elif request.form["reportType"] == 'PDF':
                                        with db_session:
                                                with db.set_perms_for(Users):
                                                        currentDateTime = datetime.now()
                                                        perm('edit create delete view', group='anybody')
                                                        leaves = namedtuple("Leaves", "LeaveID StaffName StartDate EndDate Reason ApproveResult ApprovedBy ApproveDate")
                                                        leaves = select(l for l in Leaves if l.UserID.UserID == int(session.get("user_id")) and l.StartDate.date()== l.EndDate.date())[:]
                                                        result = {'data': [{"LeaveID": p.LeaveID, "StaffName": p.UserID.FirstName+' '+p.UserID.LastName, "StartDate": p.StartDate, "EndDate": p.EndDate, "Reason": p.Reason, "ApproveResult": 'Approved' if p.IsApproved else 'Rejected' if p.IsApproved == False else 'Not Answered', "ApprovedBy":  p.ApprovedBy.FirstName+' '+p.ApprovedBy.LastName if p.ApprovedBy is not None else None, "ApproveDate": p.ApproveDate if p.ApproveDate is not None else None} for p in leaves]}
                                                        rpt = Report(result["data"])
                                                        rpt.detailband = Band([
                                                                Element((36, 0), ("Helvetica", 9), key = "StaffName"),
                                                                Element((130, 0), ("Helvetica", 9), key = "StartDate"),
                                                                Element((230, 0), ("Helvetica", 9), key = "EndDate"),
                                                                Element((330, 0), ("Helvetica", 9), key = "Reason"),
                                                                Element((430, 0), ("Helvetica", 9), key = "ApproveResult"),
                                                                Element((500, 0), ("Helvetica", 9), key = "ApprovedBy"),
                                                                Element((600, 0), ("Helvetica", 9), key = "ApproveDate"),
                                                        ])

                                                        rpt.pageheader = Band([
                                                                Element((36, 0), ("Helvetica-Bold", 20), text = "Staff's Hour Off Leave List"),
                                                                Element((36, 30), ("Helvetica", 9), text = "Staff Name"),
                                                                Element((130, 30), ("Helvetica", 9), text = "Start Date"),
                                                                Element((230, 30), ("Helvetica", 9), text = "End Date"),
                                                                Element((330, 30), ("Helvetica", 9), text = "Reason"),
                                                                Element((430, 30), ("Helvetica", 9), text = "Approve Result"),
                                                                Element((500, 30), ("Helvetica", 9), text = "Approved By"),
                                                                Element((600, 30), ("Helvetica", 9), text = "Approve Date"),
                                                                Rule((36, 42), 9*72, thickness = 2),
                                                        ])

                                                        rpt.pagefooter = Band([
                                                                Element((72*9.5, 0), ("Helvetica-Bold", 14), text = currentDateTime.strftime("%Y/%m/%d %H:%M:%S"), align = "right"),
                                                                Element((36, 16), ("Helvetica-Bold", 12), sysvar = "pagenumber", format = lambda x: "Page %d" % x),
                                                        ])
                                                        
                                                        filename = "HourOffLeaves-"+currentDateTime.strftime("%Y%m%d%H%M%S")+".pdf"
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