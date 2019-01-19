import sys
from pony.orm import *
from datetime import datetime
import configparser
config = configparser.ConfigParser()
config.sections()
config.read('config/conf.ini')

db = Database()

if config['ConnectionString']['host'] != 'NotSet' and config['ConnectionString']['database'] != 'NotSet':
    db.bind(provider=config['ConnectionString']['provider'], user=config['ConnectionString']['user'], password=config['ConnectionString']['password'], host=config['ConnectionString']['host'], database=config['ConnectionString']['database'])

class AppForms(db.Entity):
    AppFormID = PrimaryKey(int, auto=True)
    AppFormTitle = Required(str)
    RoleAccess =  Set("RoleAccesses", reverse="AppFormID")

class Roles(db.Entity):
    RoleID = PrimaryKey(int, auto=True)
    RoleTitle = Required(str)
    Description = Optional(str)
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
    Username = Required(str, unique=True)
    Password = Required(str)
    FirstName = Required(str)
    LastName = Required(str)
    PersonelCode = Required(str, unique=True)
    ManagerID = Optional("Users", reverse="employees")
    employees = Set("Users", reverse="ManagerID")
    RoleID = Required("Roles", reverse="UserRole")
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
    ApproveDate = Optional(datetime)
    LatestUpdateDate = Required(datetime)
    

class TransportTypes(db.Entity):
    TransportTypeID = PrimaryKey(int, auto=True)
    TransportTypeTitle = Required(str)
    Description = Optional(str)
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