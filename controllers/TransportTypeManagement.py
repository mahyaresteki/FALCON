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
from io import BytesIO
import pandas as pd
import numpy as np

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

@App.app.route('/TransportTypeManagement/ExportExcel', methods=['GET', 'POST'])
def ExportExcel():
        if session.get("user_id") is not None and session.get("fullname") is not None:
                if CheckAccess("Transport Types", "Print"):
                        with db_session:
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
                else:
                        return redirect("/AccessDenied", code=302)
        else:
                return redirect("/", code=302)