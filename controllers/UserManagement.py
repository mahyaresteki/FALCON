import sys
import random, json
from pony import orm
from flask import *
from flask_cors import *
import App
from models.DatabaseContext import *
import hashlib
from datetime import datetime

@App.app.route('/UserManagement/Roles')
def role_page():
    if session.get("user_id") is not None and session.get("fullname") is not None:
        with db_session:
            roles = Roles.select()
            return render_template('UserManagement/roles.html', entries = roles)
    else:
        return redirect("/", code=302)

@App.app.route('/UserManagement/CreateRole', methods=['GET', 'POST'])
@cross_origin(supports_credentials=True)
def CreateRole():
        try:
                if session.get("user_id") is not None and session.get("fullname") is not None:
                        with db_session:
                                data = request.get_json()
                                Roles(RoleTitle = data['RoleTitle'], Description = data['Description'], LatestUpdateDate = datetime.now())
                                message = "Success"
                                return jsonify({'message': message})
                else:
                        return redirect("/", code=302)
        except Exception as e:
                message = str(e)
                return jsonify({'message': message})

@App.app.route('/UserManagement/GetRole', methods=['GET', 'POST'])
@cross_origin(supports_credentials=True)
def GetRole():
    if session.get("user_id") is not None and session.get("fullname") is not None:
        with db_session:
            data = request.get_json()
            query= Roles.select(lambda u: u.RoleID == int(data['RoleID']))
            mylist = list(query)
            return jsonify({'RoleID': mylist[0].RoleID, 'RoleTitle': mylist[0].RoleTitle, 'Description': mylist[0].Description})
    else:
        return redirect("/", code=302)


@App.app.route('/UserManagement/DeleteRole', methods=['GET', 'POST'])
@cross_origin(supports_credentials=True)
def DeleteRole():
        try:
                if session.get("user_id") is not None and session.get("fullname") is not None:
                        with db_session:
                                data = request.get_json()
                                delete(p for p in Roles if p.RoleID == int(data["RoleID"]))
                                message = "Success"
                                return jsonify({'message': message})
                else:
                        return redirect("/", code=302)
        except Exception as e:
                message = str(e)
                return jsonify({'message': message})


@App.app.route('/UserManagement/EditRole', methods=['GET', 'POST'])
@cross_origin(supports_credentials=True)
def EditRole():
        try:
                if session.get("user_id") is not None and session.get("fullname") is not None:
                        with db_session:
                                data = request.get_json()
                                role = Roles[int(data['RoleID'])]
                                role.set(RoleTitle = data['RoleTitle'], Description = data['Description'], LatestUpdateDate = datetime.now())
                                message = "Success"
                                return jsonify({'message': message})
                else:
                        return redirect("/", code=302)
        except Exception as e:
                message = str(e)
                return jsonify({'message': message})


@App.app.route('/UserManagement/RoleAccesses')
def role_access_page():
    if session.get("user_id") is not None and session.get("fullname") is not None:
        with db_session:
            roles = Roles.select()
            return render_template('UserManagement/roleaccesses.html', roles = roles)
    else:
        return redirect("/", code=302)


@App.app.route('/UserManagement/GetRoleAccesses', methods=['GET', 'POST'])
@cross_origin(supports_credentials=True)
def GetRoleAccesses():
    if session.get("user_id") is not None and session.get("fullname") is not None:
        with db_session:
            data = request.get_json()
            id = int(data["RoleID"])
            query= db.select('''SELECT r.roleid, r.roletitle, af.appformid, af.appformtitle, ra.creategrant, ra.ReadGrant, ra.UpdateGrant, ra.DeleteGrant, ra.PrintGrant
                FROM public.appforms as af cross join public.roles as r
                full outer join public.roleaccesses as ra on af.appformid = ra.appformid and r.roleid = ra.roleid
                WHERE r.roleid='''+str(id) +'order by r.roleid, af.appformid' )
            mylist = list(query)
            return jsonify(mylist)
    else:
        return redirect("/", code=302)


@App.app.route('/UserManagement/SetRoleAccesses', methods=['GET', 'POST'])
@cross_origin(supports_credentials=True)
def SetRoleAccesses():
        try:
                if session.get("user_id") is not None and session.get("fullname") is not None:
                        with db_session:
                                data = request.get_json()
                                Accesses = data["Accesses"]
                                for item in Accesses:
                                        query = RoleAccesses.select(lambda u: u.RoleID.RoleID == int(item['roleId']) and u.AppFormID.AppFormID == int(item['formId']))
                                        mylist = list(query)
                                        if len(mylist) > 0:
                                                roleAccess = RoleAccesses[mylist[0].RoleAccessID]
                                                roleAccess.set(CreateGrant = bool(item["create"]), ReadGrant = bool(item["read"]), UpdateGrant = bool(item["update"]), DeleteGrant = bool(item["delete"]), PrintGrant = bool(item["print"]), LatestUpdateDate = datetime.now() )
                                        else:
                                                RoleAccesses(RoleID = int(item["roleId"]), AppFormID = int(item["formId"]), CreateGrant = bool(item["create"]), ReadGrant = bool(item["read"]), UpdateGrant = bool(item["update"]), DeleteGrant = bool(item["delete"]), PrintGrant = bool(item["print"]), LatestUpdateDate = datetime.now() )
                                message = "Success"
                                return jsonify({'message': message})
                else:
                        return redirect("/", code=302)
        except Exception as e:
                message = str(e)
                return jsonify({'message': message})


@App.app.route('/UserManagement/Users')
def user_page():
    if session.get("user_id") is not None and session.get("fullname") is not None:
        with db_session:
            users = Users.select()
            roles = Roles.select()
            return render_template('UserManagement/users.html', users = users, roles = roles)
    else:
        return redirect("/", code=302)


@App.app.route('/UserManagement/CreateUser', methods=['GET', 'POST'])
@cross_origin(supports_credentials=True)
def CreateUser():
        try:
                if session.get("user_id") is not None and session.get("fullname") is not None:
                        with db_session:
                                data = request.get_json()
                                print(data['Password'])
                                password = hashlib.sha512(str(data['Password']).encode('utf-8')).hexdigest()
                                Users(FirstName = str(data['FirstName']), LastName =str(data['LastName']), Username=str(data['Username']), Password=password, RoleID=int(data['RoleID']), PersonelCode=str(data['PersonelCode']), IsActive=True, LatestUpdateDate = datetime.now() )
                                message = "Success"
                                return jsonify({'message': message})
                else:
                        return redirect("/", code=302)
        except Exception as e:
                message = str(e)
                return jsonify({'message': message})


@App.app.route('/UserManagement/GetUser', methods=['GET', 'POST'])
@cross_origin(supports_credentials=True)
def GetUser():
    if session.get("user_id") is not None and session.get("fullname") is not None:
        with db_session:
            data = request.get_json()
            query= Users.select(lambda u: u.UserID == int(data['UserID']))
            mylist = list(query)
            return jsonify({'UserID': mylist[0].UserID, 'FirstName': mylist[0].FirstName, 'LastName': mylist[0].LastName, 'Username': mylist[0].Username, 'RoleID': mylist[0].RoleID.RoleID, 'RoleTitle': mylist[0].RoleID.RoleTitle, 'PersonelCode': mylist[0].PersonelCode})
    else:
        return redirect("/", code=302)



@App.app.route('/UserManagement/DeleteUser', methods=['GET', 'POST'])
@cross_origin(supports_credentials=True)
def DeleteUser():
        try:
                if session.get("user_id") is not None and session.get("fullname") is not None:
                        with db_session:
                                data = request.get_json()
                                delete(p for p in Users if p.UserID == int(data["UserID"]))
                                message = "Success"
                                return jsonify({'message': message})
                else:
                        return redirect("/", code=302)
        except Exception as e:
                message = str(e)
                return jsonify({'message': message})


@App.app.route('/UserManagement/EditUser', methods=['GET', 'POST'])
@cross_origin(supports_credentials=True)
def EditUser():
        try:
                if session.get("user_id") is not None and session.get("fullname") is not None:
                        with db_session:
                                data = request.get_json()
                                user = Users[int(data['UserID'])]
                                user.set(FirstName = str(data['FirstName']), LastName =str(data['LastName']), Username=str(data['Username']), RoleID=int(data['RoleID']), PersonelCode=str(data['PersonelCode']), IsActive=True, LatestUpdateDate = datetime.now())
                                message = "Success"
                                return jsonify({'message': message})
                else:
                        return redirect("/", code=302)
        except Exception as e:
                message = str(e)
                return jsonify({'message': message})


@App.app.route('/UserManagement/UserActivation', methods=['GET', 'POST'])
@cross_origin(supports_credentials=True)
def UserActivation():
        try:
                if session.get("user_id") is not None and session.get("fullname") is not None:
                        with db_session:
                                data = request.get_json()
                                user = Users[int(data['UserID'])]
                                if user.IsActive:
                                        user.set(IsActive=False, LatestUpdateDate = datetime.now())
                                else:
                                        user.set(IsActive=True, LatestUpdateDate = datetime.now())
                                message = "Success"
                                return jsonify({'message': message})
                else:
                        return redirect("/", code=302)
        except Exception as e:
                message = str(e)
                return jsonify({'message': message})

@App.app.route('/UserManagement/ChangePasswordByAdmin', methods=['GET', 'POST'])
@cross_origin(supports_credentials=True)
def ChangePasswordByAdmin():
        try:
                if session.get("user_id") is not None and session.get("fullname") is not None:
                        with db_session:
                                data = request.get_json()
                                user = Users[int(data['UserID'])]
                                oldPassword = hashlib.sha512(str(data['OldPassword']).encode('utf-8')).hexdigest()
                                message = ""
                                if user.Password == oldPassword:
                                        newPassword = hashlib.sha512(str(data['NewPassword']).encode('utf-8')).hexdigest()
                                        user.set(Password = newPassword, LatestUpdateDate = datetime.now())
                                        message = "Success"
                                else:
                                        message = "The old password is not correct"
                                return jsonify({'message': message})
                else:
                        return redirect("/", code=302)
        except Exception as e:
                message = str(e)
                return jsonify({'message': message})