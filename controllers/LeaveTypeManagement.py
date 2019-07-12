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

@App.app.route('/LeaveTypeManagement/LeaveTypes')
def leavetype_page():
    if session.get("user_id") is not None and session.get("fullname") is not None:
        if CheckAccess("Leave Types", "Read"):
                with db_session:
                        search = False
                        page = request.args.get(get_page_parameter(), type=int, default=1)
                        leaveTypes = LeaveTypes.select()
                        pagination = Pagination(page=page, total=leaveTypes.count(), search=search, record_name='leave types', css_framework='bootstrap4')
                        return render_template('LeaveTypeManagement/leavetypes.html', leaveTypes = leaveTypes.page(page, 10), pagination=pagination, formAccess = GetFormAccessControl("Leave Types"))
        else:
                return redirect("/AccessDenied", code=302)
    else:
        return redirect("/", code=302)

@App.app.route('/LeaveTypeManagement/CreateLeaveType', methods=['GET', 'POST'])
@cross_origin(supports_credentials=True)
def CreateLeaveType():
        try:
                if session.get("user_id") is not None and session.get("fullname") is not None:
                        if CheckAccess("Leave Types", "Create"):
                                with db.set_perms_for(LeaveTypes):
                                        perm('edit create delete view', group='anybody')
                                        with db_session:
                                                data = request.get_json()
                                                leaveTypes = LeaveTypes(TransportTypeTitle = data['LeaveTypeTitle'], SalaryRatio = float(data['SalaryRatio']), Description = data['Description'], LatestUpdateDate = datetime.now())
                                                commit()
                                                message = "Success"
                                                j = json.loads(leaveTypes.to_json())
                                                InsertInfoLog('create', 'leave type', 'LeaveTypes', j, str(leaveTypes.LeaveTypeID))
                                                return jsonify({'message': message})
                        else:
                                return redirect("/AccessDenied", code=302)
                else:
                        return redirect("/", code=302)
        except Exception as e:
                InsertErrorLog('leave type', 'create')
                message = str(e)
                return jsonify({'message': message})


@App.app.route('/LeaveTypeManagement/GetLeaveType', methods=['GET', 'POST'])
@cross_origin(supports_credentials=True)
def GetLeaveType():
    if session.get("user_id") is not None and session.get("fullname") is not None:
        with db_session:
            data = request.get_json()
            query= LeaveTypes.select(lambda u: u.LeaveTypeID == int(data['LeaveTypeID']))
            mylist = list(query)
            return jsonify({'LeaveTypeID': mylist[0].LeaveTypeID, 'LeaveTypeTitle': mylist[0].LeaveTypeTitle, 'SalaryRatio': mylist[0].SalaryRatio, 'Description': mylist[0].Description})
    else:
        return redirect("/", code=302)


@App.app.route('/LeaveTypeManagement/DeleteLeaveType', methods=['GET', 'POST'])
@cross_origin(supports_credentials=True)
def DeleteLeaveType():
        try:
                if session.get("user_id") is not None and session.get("fullname") is not None:
                        if CheckAccess("Leave Types", "Delete"):
                                with db_session:
                                        with db.set_perms_for(LeaveTypes):
                                                perm('edit create delete view', group='anybody')
                                                data = request.get_json()
                                                leaveTypes = LeaveTypes.select(lambda tt: tt.LeaveTypeID == int(data["LeaveTypeID"]))
                                                j = json.loads(leaveTypes.to_json())
                                                delete(p for p in LeaveTypes if p.LeaveTypeID == int(data["LeaveTypeID"]))
                                                commit()
                                                message = "Success"
                                                InsertInfoLog('delete', 'leave type', 'LeaveTypes', j,str(data["LeaveTypeID"]))
                                                return jsonify({'message': message})
                        else:
                                return redirect("/AccessDenied", code=302)
                else:
                        return redirect("/", code=302)
        except Exception as e:
                InsertErrorLog('leave type', 'delete')
                message = str(e)
                return jsonify({'message': message})


@App.app.route('/LeaveTypeManagement/EditLeaveType', methods=['GET', 'POST'])
@cross_origin(supports_credentials=True)
def EditLeaveType():
        try:
                if session.get("user_id") is not None and session.get("fullname") is not None:
                        if CheckAccess("Leave Types", "Update"):
                                with db_session:
                                        with db.set_perms_for(LeaveTypes):
                                                perm('edit create delete view', group='anybody')
                                                data = request.get_json()
                                                leaveTypes = LeaveTypes[int(data['LeaveTypeID'])]
                                                leaveTypes.set(LeaveTypeTitle = data['LeaveTypeTitle'], SalaryRatio = float(data['SalaryRatio']), Description = data['Description'], LatestUpdateDate = datetime.now())
                                                commit()
                                                j = json.loads(leaveTypes.to_json())
                                                InsertInfoLog('update', 'leave type', 'LeaveTypes', j,str(data["LeaveTypeID"]))
                                                message = "Success"
                                                return jsonify({'message': message})
                        else:
                                return redirect("/AccessDenied", code=302)
                else:
                        return redirect("/", code=302)
        except Exception as e:
                InsertErrorLog('leave type', 'update')
                message = str(e)
                return jsonify({'message': message})

@App.app.route('/LeaveTypeManagement/ExportReport', methods=['GET', 'POST'])
def LeaveTypeExportReport():
        if session.get("user_id") is not None and session.get("fullname") is not None:
                if CheckAccess("Leave Types", "Print"):
                        with db_session:
                                if request.form["reportType"] == 'Excel':
                                        output = BytesIO()
                                        writer = pd.ExcelWriter(output, engine='xlsxwriter')
                                        workbook = writer.book
                                        worksheet = workbook.add_worksheet()
                                        bold = workbook.add_format({'bold': True})
                                        worksheet.write('A1', 'No.', bold)
                                        worksheet.write('B1', 'Leave Type Title', bold)
                                        worksheet.write('C1', 'Salary Ratio', bold)
                                        worksheet.write('D1', 'Description', bold)
                                        row = 1
                                        col = 0
                                        leaveTypes = LeaveTypes.select()
                                        for item in leaveTypes:
                                                worksheet.write(row, col, row)
                                                worksheet.write(row, col + 1, item.LeaveTypeTitle)
                                                worksheet.write(row, col + 2, item.SalaryRatio)
                                                worksheet.write(row, col + 3, item.Description)
                                                row += 1
                                        writer.close()
                                        output.seek(0)
                                        return send_file(output, attachment_filename="LeaveTypes-"+datetime.now().strftime("%Y%m%d%H%M%S")+".xlsx", as_attachment=True)
                                elif request.form["reportType"] == 'CVS':
                                        def generate():
                                                with db_session:
                                                        output = StringIO()
                                                        writer = csv.writer(output)
                                                        writer.writerow(('Title','Salary Ratio', 'Description'))
                                                        yield output.getvalue()
                                                        output.seek(0)
                                                        output.truncate(0)
                                                        leaveTypes = LeaveTypes.select()
                                                        for item in leaveTypes:
                                                                writer.writerow((item.LeaveTypeTitle,item.SalaryRatio,item.Description))
                                                                yield output.getvalue()
                                                                output.seek(0)
                                                                output.truncate(0)
                                        headers = Headers()
                                        headers.set('Content-Disposition', 'attachment', filename="LeaveTypes-"+datetime.now().strftime("%Y%m%d%H%M%S")+".cvs")

                                        return Response(
                                                        stream_with_context(generate()),
                                                        mimetype='text/csv', headers=headers
                                        )
                                elif request.form["reportType"] == 'PDF':
                                        with db_session:
                                                with db.set_perms_for(TransportTypes):
                                                        currentDateTime = datetime.now()
                                                        perm('edit create delete view', group='anybody')
                                                        leaveTypes = namedtuple("LeaveTypes", "LeaveTypeID LeaveTypeTitle SalaryRatio Description")
                                                        leaveTypes = select(lt for lt in LeaveTypes)[:]
                                                        result = {'data': [{"LeaveTypeID": p.TransportTypeID, "LeaveTypeTitle": p.LeaveTypeTitle, "Description": p.Description} for p in leaveTypes]}
                                                        rpt = Report(result["data"])
                                                        rpt.detailband = Band([
                                                                Element((36, 0), ("Helvetica", 11), key = "LeaveTypeTitle"),
                                                                Element((300, 0), ("Helvetica", 11), key = "SalaryRatio"),
                                                                Element((566, 0), ("Helvetica", 11), key = "Description"),
                                                        ])

                                                        rpt.pageheader = Band([
                                                                Element((36, 0), ("Helvetica-Bold", 20), text = "Leave Type List"),
                                                                Element((36, 24), ("Helvetica", 12), text = "Title"),
                                                                Element((300, 24), ("Helvetica", 12), text = "Salary Ratio"),
                                                                Element((566, 24), ("Helvetica", 12), text = "Description"),
                                                                Rule((36, 42), 6.5*72, thickness = 2),
                                                        ])

                                                        rpt.pagefooter = Band([
                                                                Element((72*7, 0), ("Helvetica-Bold", 14), text = currentDateTime.strftime("%Y/%m/%d %H:%M:%S"), align = "right"),
                                                                Element((36, 16), ("Helvetica-Bold", 12), sysvar = "pagenumber", format = lambda x: "Page %d" % x),
                                                        ])
                                                        
                                                        filename = "LeavefTypes-"+currentDateTime.strftime("%Y%m%d%H%M%S")+".pdf"
                                                        output = BytesIO()
                                                        canvas = Canvas(output, (72*8.5, 72*11))
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