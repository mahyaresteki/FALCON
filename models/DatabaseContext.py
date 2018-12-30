import sys
from pony.orm import *
from datetime import datetime

db = Database()

db.bind(provider='postgres', user='postgres', password='123456', host='127.0.0.1', database='FALCON_DB')

class AppForms(db.Entity):
    AppFormID = PrimaryKey(int, auto=True)
    AppFormTitle = Required(str)
    RoleAccess =  Set("RoleAccesses", reverse="AppFormID")

class Roles(db.Entity):
    RoleID = PrimaryKey(int, auto=True)
    RoleTitle = Required(str)
    Description = Required(str)
    LatestUpdateDate = Required(datetime)
    UserRole = Set("Users", reverse="RoleID")
    RoleAccess =  Set("RoleAccesses", reverse="RoleID")

class RoleAccesses(db.Entity):
    RoleAccessID = PrimaryKey(int, auto=True)
    AppFormID = Optional("AppForms", reverse="RoleAccess")
    RoleID = Optional("Roles", reverse="RoleAccess")
    CreateGrant = Required(bool)
    ReadGrant = Required(bool)
    UpdateGrant = Required(bool)
    DeleteGrant = Required(bool)
    PrintGrant = Required(bool)
    LatestUpdateDate = Required(datetime)

class Users(db.Entity):
    UserID = PrimaryKey(int, auto=True)
    Username = Required(str)
    Password = Required(str)
    FirstName = Required(str)
    LastName = Required(str)
    ManagerID = Optional("Users", reverse="ManagerID")
    RoleID = Optional("Roles", reverse="UserRole")
    IsActive = Required(bool)
    LatestUpdateDate = Required(datetime)
    LeaveRequester = Set("Leaves", reverse="UserID")
    LeaveApproval = Set("Leaves", reverse="ApprovedBy")
    MissionRequester = Set("Missions", reverse="UserID")
    MissionApproval = Set("Missions", reverse="ApprovedBy")




class Leaves(db.Entity):
    LeaveID = PrimaryKey(int, auto=True)
    UserID = Required(Users, reverse="LeaveRequester")
    StartDate = Required(datetime)
    EndDate = Required(datetime)
    ApprovedBy = Optional(Users, reverse="LeaveApproval")
    LatestUpdateDate = Required(datetime)
    

class TransportTypes(db.Entity):
    TransportTypeID = PrimaryKey(int, auto=True)
    TransportTypeTitle = Required(str)
    Description = Required(str)
    LatestUpdateDate = Required(datetime)
    MissionTransportWent = Set("Missions", reverse="TransportTypeWentID")
    MissionTransportReturn = Set("Missions", reverse="TransportTypeReturnID")


class Missions(db.Entity):
    MessionID = PrimaryKey(int, auto=True)
    UserID = Required(Users, reverse="MissionRequester")
    StartDate = Required(datetime)
    EndDate = Required(datetime)
    TransportTypeWentID = Optional(TransportTypes, reverse="MissionTransportWent")
    WentPayment = Optional(float)
    TransportTypeReturnID = Optional(TransportTypes, reverse="MissionTransportReturn")
    ReturnPayment = Optional(float)
    ApprovedBy = Optional(Users, reverse="MissionApproval")
    LatestUpdateDate = Required(datetime)