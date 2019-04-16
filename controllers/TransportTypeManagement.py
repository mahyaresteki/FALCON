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

@App.app.route('/TransportTypeManagement/TransportTypes')
def transporttype_page():
    if session.get("user_id") is not None and session.get("fullname") is not None:
        if CheckAccess("Transport Types", "Read"):
                with db_session:
                        search = False
                        page = request.args.get(get_page_parameter(), type=int, default=1)
                        transportTypes = TransportTypes.select()
                        pagination = Pagination(page=page, total=transportTypes.count(), search=search, record_name='transport types', css_framework='bootstrap4')
                        return render_template('TransportTypeManagement/transporttypes.html', transportTypes = transportTypes.page(page, 10), pagination=pagination, formAccess = GetFormAccessControl("Transport Types"))
        else:
                return redirect("/AccessDenied", code=302)
    else:
        return redirect("/", code=302)

@App.app.route('/TransportTypeManagement/CreateTransportType', methods=['GET', 'POST'])
@cross_origin(supports_credentials=True)
def CreateTransportType():
        try:
                if session.get("user_id") is not None and session.get("fullname") is not None:
                        if CheckAccess("Transport Types", "Create"):
                                with db.set_perms_for(TransportTypes):
                                        perm('edit create delete view', group='anybody')
                                        with db_session:
                                                data = request.get_json()
                                                transportTypes = TransportTypes(TransportTypeTitle = data['TransportTypeTitle'], Description = data['Description'], LatestUpdateDate = datetime.now())
                                                commit()
                                                message = "Success"
                                                j = json.loads(transportTypes.to_json())
                                                InsertInfoLog('create', 'transport type', 'TransportTypes', j, str(transportTypes.TransportTypeID))
                                                return jsonify({'message': message})
                        else:
                                return redirect("/AccessDenied", code=302)
                else:
                        return redirect("/", code=302)
        except Exception as e:
                InsertErrorLog('transport type', 'create')
                message = str(e)
                return jsonify({'message': message})

@App.app.route('/TransportTypeManagement/GetTransportType', methods=['GET', 'POST'])
@cross_origin(supports_credentials=True)
def GetTransportType():
    if session.get("user_id") is not None and session.get("fullname") is not None:
        with db_session:
            data = request.get_json()
            query= TransportTypes.select(lambda u: u.TransportTypeID == int(data['TransportTypeID']))
            mylist = list(query)
            return jsonify({'TransportTypeID': mylist[0].TransportTypeID, 'TransportTypeTitle': mylist[0].TransportTypeTitle, 'Description': mylist[0].Description})
    else:
        return redirect("/", code=302)


@App.app.route('/TransportTypeManagement/DeleteTransportType', methods=['GET', 'POST'])
@cross_origin(supports_credentials=True)
def DeleteTransportType():
        try:
                if session.get("user_id") is not None and session.get("fullname") is not None:
                        if CheckAccess("Transport Types", "Delete"):
                                with db_session:
                                        with db.set_perms_for(TransportTypes):
                                                perm('edit create delete view', group='anybody')
                                                data = request.get_json()
                                                transportTypes = TransportTypes.select(lambda tt: tt.TransportTypeID == int(data["TransportTypeID"]))
                                                j = json.loads(transportTypes.to_json())
                                                delete(p for p in TransportTypes if p.TransportTypeID == int(data["TransportTypeID"]))
                                                commit()
                                                message = "Success"
                                                InsertInfoLog('delete', 'transport type', 'TransportTypes', j,str(data["TransportTypeID"]))
                                                return jsonify({'message': message})
                        else:
                                return redirect("/AccessDenied", code=302)
                else:
                        return redirect("/", code=302)
        except Exception as e:
                InsertErrorLog('transport type', 'delete')
                message = str(e)
                return jsonify({'message': message})


@App.app.route('/TransportTypeManagement/EditTransportType', methods=['GET', 'POST'])
@cross_origin(supports_credentials=True)
def EditTransportType():
        try:
                if session.get("user_id") is not None and session.get("fullname") is not None:
                        if CheckAccess("Transport Types", "Update"):
                                with db_session:
                                        with db.set_perms_for(TransportTypes):
                                                perm('edit create delete view', group='anybody')
                                                data = request.get_json()
                                                transportTypes = TransportTypes[int(data['TransportTypeID'])]
                                                transportTypes.set(TransportTypeTitle = data['TransportTypeTitle'], Description = data['Description'], LatestUpdateDate = datetime.now())
                                                commit()
                                                j = json.loads(transportTypes.to_json())
                                                InsertInfoLog('update', 'transport type', 'TransportTypes', j,str(data["TransportTypeID"]))
                                                message = "Success"
                                                return jsonify({'message': message})
                        else:
                                return redirect("/AccessDenied", code=302)
                else:
                        return redirect("/", code=302)
        except Exception as e:
                InsertErrorLog('transport type', 'update')
                message = str(e)
                return jsonify({'message': message})

@App.app.route('/TransportTypeManagement/ExportReport', methods=['GET', 'POST'])
def TransportTypeExportReport():
        if session.get("user_id") is not None and session.get("fullname") is not None:
                if CheckAccess("Transport Types", "Print"):
                        with db_session:
                                if request.form["reportType"] == 'Excel':
                                        output = BytesIO()
                                        writer = pd.ExcelWriter(output, engine='xlsxwriter')
                                        workbook = writer.book
                                        worksheet = workbook.add_worksheet()
                                        bold = workbook.add_format({'bold': True})
                                        worksheet.write('A1', 'No.', bold)
                                        worksheet.write('B1', 'Transport Type Title', bold)
                                        worksheet.write('C1', 'Description', bold)
                                        row = 1
                                        col = 0
                                        transportTypes = TransportTypes.select()
                                        for item in transportTypes:
                                                worksheet.write(row, col, row)
                                                worksheet.write(row, col + 1, item.TransportTypeTitle)
                                                worksheet.write(row, col + 2, item.Description)
                                                row += 1
                                        writer.close()
                                        output.seek(0)
                                        return send_file(output, attachment_filename="TransportTypes-"+datetime.now().strftime("%Y%m%d%H%M%S")+".xlsx", as_attachment=True)
                                elif request.form["reportType"] == 'CVS':
                                        def generate():
                                                with db_session:
                                                        output = StringIO()
                                                        writer = csv.writer(output)
                                                        writer.writerow(('Title', 'Description'))
                                                        yield output.getvalue()
                                                        output.seek(0)
                                                        output.truncate(0)
                                                        transportTypes = TransportTypes.select()
                                                        for item in transportTypes:
                                                                writer.writerow((item.TransportTypeTitle,item.Description))
                                                                yield output.getvalue()
                                                                output.seek(0)
                                                                output.truncate(0)
                                        headers = Headers()
                                        headers.set('Content-Disposition', 'attachment', filename="TransportTypes-"+datetime.now().strftime("%Y%m%d%H%M%S")+".cvs")

                                        return Response(
                                                        stream_with_context(generate()),
                                                        mimetype='text/csv', headers=headers
                                        )
                                elif request.form["reportType"] == 'PDF':
                                        with db_session:
                                                with db.set_perms_for(TransportTypes):
                                                        currentDateTime = datetime.now()
                                                        perm('edit create delete view', group='anybody')
                                                        transportTypes = namedtuple("TransportTypes", "TransportTypeID TransportTypeTitle Description")
                                                        transportTypes = select(tt for tt in TransportTypes)[:]
                                                        result = {'data': [{"TransportTypeID": p.TransportTypeID, "TransportTypeTitle": p.TransportTypeTitle, "Description": p.Description} for p in transportTypes]}
                                                        rpt = Report(result["data"])
                                                        rpt.detailband = Band([
                                                                Element((36, 0), ("Helvetica", 11), key = "TransportTypeTitle"),
                                                                Element((300, 0), ("Helvetica", 11), key = "Description"),
                                                        ])

                                                        rpt.pageheader = Band([
                                                                Element((36, 0), ("Helvetica-Bold", 20), text = "Transport Type List"),
                                                                Element((36, 24), ("Helvetica", 12), text = "Title"),
                                                                Element((300, 24), ("Helvetica", 12), text = "Description"),
                                                                Rule((36, 42), 6.5*72, thickness = 2),
                                                        ])

                                                        rpt.pagefooter = Band([
                                                                Element((72*7, 0), ("Helvetica-Bold", 14), text = currentDateTime.strftime("%Y/%m/%d %H:%M:%S"), align = "right"),
                                                                Element((36, 16), ("Helvetica-Bold", 12), sysvar = "pagenumber", format = lambda x: "Page %d" % x),
                                                        ])
                                                        
                                                        filename = "TransportTypes-"+currentDateTime.strftime("%Y%m%d%H%M%S")+".pdf"
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