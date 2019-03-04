import sys
import random, json
from pony import orm
from flask import *
from flask_cors import *
import App
from models.DatabaseContext import *
import hashlib
from datetime import datetime
from controllers.Security import CheckAccess, GetFormAccessControl

@App.app.route('/TransportTypeManagement/TransportTypes')
def transporttype_page():
    if session.get("user_id") is not None and session.get("fullname") is not None:
        if CheckAccess("Transport Types", "Read"):
                with db_session:
                        transportTypes = TransportTypes.select()
                        return render_template('TransportTypeManagement/transporttypes.html', entries = transportTypes, formAccess = GetFormAccessControl("Transport Types"))
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
                                with db_session:
                                        data = request.get_json()
                                        TransportTypes(TransportTypeTitle = data['TransportTypeTitle'], Description = data['Description'], LatestUpdateDate = datetime.now())
                                        message = "Success"
                                        return jsonify({'message': message})
                        else:
                                return redirect("/AccessDenied", code=302)
                else:
                        return redirect("/", code=302)
        except Exception as e:
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
                                        data = request.get_json()
                                        delete(p for p in TransportTypes if p.TransportTypeID == int(data["TransportTypeID"]))
                                        message = "Success"
                                        return jsonify({'message': message})
                        else:
                                return redirect("/AccessDenied", code=302)
                else:
                        return redirect("/", code=302)
        except Exception as e:
                message = str(e)
                return jsonify({'message': message})


@App.app.route('/TransportTypeManagement/EditTransportType', methods=['GET', 'POST'])
@cross_origin(supports_credentials=True)
def EditTransportType():
        try:
                if session.get("user_id") is not None and session.get("fullname") is not None:
                        if CheckAccess("Transport Types", "Update"):
                                with db_session:
                                        data = request.get_json()
                                        role = TransportTypes[int(data['TransportTypeID'])]
                                        role.set(TransportTypeTitle = data['TransportTypeTitle'], Description = data['Description'], LatestUpdateDate = datetime.now())
                                        message = "Success"
                                        return jsonify({'message': message})
                        else:
                                return redirect("/AccessDenied", code=302)
                else:
                        return redirect("/", code=302)
        except Exception as e:
                message = str(e)
                return jsonify({'message': message})