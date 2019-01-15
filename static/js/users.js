var result = {};

function CreateUser(FirstName, LastName, Username, Password, RoleID, PersonelCode, ManagerID)
{
    $.ajaxSetup({
        type: "POST",
        data: {},
        dataType: 'json',
        xhrFields: {
            withCredentials: true
        },
        crossDomain: true,
        contentType: 'application/json; charset=utf-8'
    });

    var jsondata =	{
        "FirstName": FirstName,
        "LastName": LastName,
        "Username": Username,
        "Password": Password,
        "RoleID": RoleID,
        "PersonelCode": PersonelCode,
        "ManagerID": ManagerID
    };
    var a = JSON.stringify(jsondata);

    $.ajax({
        url: '/UserManagement/CreateUser',
        type: 'POST',
        dataType: 'json',
        crossDomain: true,
        headers: {
            'Access-Control-Allow-Origin': '*',
            "Accept" : "application/json"
        },
        contentType: "application/json; charset=utf-8",
        data: a,
        success: function (data) {
            if (data['message'] == "Success") {
                $('#CreateEditModal').hide();
                $('#CreateEditModal #FirstName').val('');
                $('#CreateEditModal #LastName').val('');
                $('#CreateEditModal #RoleID').val('');
                $('#CreateEditModal #Username').val('');
                $('#CreateEditModal #Password').val('');
                $('#CreateEditModal #ConfirmPassword').val('');
                $('#CreateEditModal #PersonelCode').val('');
                $('#CreateEditModal #ManagerID').val('');
                location.reload();
            }
            else
            {
                alert(data['message']);
            }
        },
        error: function (data, xmlHttpRequest, errorText, thrownError) {
            alert(errorText);
        }
    });
}

function ChangePassword(UserID, Password)
{
    $.ajaxSetup({
        type: "POST",
        data: {},
        dataType: 'json',
        xhrFields: {
            withCredentials: true
        },
        crossDomain: true,
        contentType: 'application/json; charset=utf-8'
    });

    var jsondata =	{
        "UserID": UserID,
        "Password": Password
    };
    var a = JSON.stringify(jsondata);

    $.ajax({
        url: '/UserManagement/ChangePasswordByAdmin',
        type: 'POST',
        dataType: 'json',
        crossDomain: true,
        headers: {
            'Access-Control-Allow-Origin': '*',
            "Accept" : "application/json"
        },
        contentType: "application/json; charset=utf-8",
        data: a,
        success: function (data) {
            if (data['message'] == "Success") {
                $('#ChangePasswordModal').hide();
                $('#ChangePasswordModal #Password').val('');
                $('#ChangePasswordModal #ConfirmPassword').val('');
                location.reload();
            }
            else
            {
                alert(data['message']);
            }
        },
        error: function (data, xmlHttpRequest, errorText, thrownError) {
            alert(errorText);
        }
    });
}

function GetUser(UserID)
{
    $.ajaxSetup({
        type: "POST",
        data: {},
        dataType: 'json',
        xhrFields: {
            withCredentials: true
        },
        crossDomain: true,
        contentType: 'application/json; charset=utf-8'
    });

    var jsondata =	{
        "UserID": UserID
    };
    var a = JSON.stringify(jsondata);

    $.ajax({
        url: '/UserManagement/GetUser',
        type: 'POST',
        dataType: 'json',
        crossDomain: true,
        headers: {
            'Access-Control-Allow-Origin': '*',
            "Accept" : "application/json"
        },
        contentType: "application/json; charset=utf-8",
        data: a,
        success: function (data) {
            result = data;
        },
        error: function (data, xmlHttpRequest, errorText, thrownError) {
            result = errorText;
        }
    });
}


function DeleteUser(UserID)
{
    $.ajaxSetup({
        type: "POST",
        data: {},
        dataType: 'json',
        xhrFields: {
            withCredentials: true
        },
        crossDomain: true,
        contentType: 'application/json; charset=utf-8'
    });

    var jsondata =	{
        "UserID": UserID
    };
    var a = JSON.stringify(jsondata);

    $.ajax({
        url: '/UserManagement/DeleteUser',
        type: 'POST',
        dataType: 'json',
        crossDomain: true,
        headers: {
            'Access-Control-Allow-Origin': '*',
            "Accept" : "application/json"
        },
        contentType: "application/json; charset=utf-8",
        data: a,
        success: function (data) {
            if (data['message'] == "Success") {
                $('#DeleteModal').hide();
                $('#DeleteModal #RoleTitle').html('');
                $('#DeleteModal #FirstName').html('');
                $('#DeleteModal #LastName').html('');
                $('#DeleteModal #RoleTitle').html('');
                $('#DeleteModal #ManagerName').html('');
                $('#DeleteModal #Username').html('');
                $('#DeleteModal #PersonelCode').html('');
                location.reload();
            }
            else
            {
                alert(data['message']);
            }
        },
        error: function (data, xmlHttpRequest, errorText, thrownError) {
            alert(errorText);
        }
    });
}

function EditUser(UserID, FirstName, LastName, Username, RoleID, PersonelCode, ManagerID)
{
    $.ajaxSetup({
        type: "POST",
        data: {},
        dataType: 'json',
        xhrFields: {
            withCredentials: true
        },
        crossDomain: true,
        contentType: 'application/json; charset=utf-8'
    });
    var jsondata =	{
        "UserID": UserID,
        "FirstName": FirstName,
        "LastName": LastName,
        "Username": Username,
        "RoleID": RoleID,
        "PersonelCode": PersonelCode,
        "ManagerID": ManagerID
    };
    var a = JSON.stringify(jsondata);

    $.ajax({
        url: '/UserManagement/EditUser',
        type: 'POST',
        dataType: 'json',
        crossDomain: true,
        headers: {
            'Access-Control-Allow-Origin': '*',
            "Accept" : "application/json"
        },
        contentType: "application/json; charset=utf-8",
        data: a,
        success: function (data) {
            if (data['message'] == "Success") {
                $('#CreateEditModal').hide();
                $('#CreateEditModal #FirstName').val('');
                $('#CreateEditModal #LastName').val('');
                $('#CreateEditModal #RoleID').val('');
                $('#CreateEditModal #ManagerID').val('');
                $('#CreateEditModal #Username').val('');
                $('#CreateEditModal #Password').val('');
                $('#CreateEditModal #ConfirmPassword').val('');
                $('#CreateEditModal #PersonelCode').val('');
                location.reload();
            }
            else
            {
                alert(data['message']);
            }
        },
        error: function (data, xmlHttpRequest, errorText, thrownError) {
            alert(data.responseText);
        }
    });
}


function UserActivate(UserID)
{
    $.ajaxSetup({
        type: "POST",
        data: {},
        dataType: 'json',
        xhrFields: {
            withCredentials: true
        },
        crossDomain: true,
        contentType: 'application/json; charset=utf-8'
    });

    var jsondata =	{
        "UserID": UserID
    };
    var a = JSON.stringify(jsondata);

    $.ajax({
        url: '/UserManagement/UserActivation',
        type: 'POST',
        dataType: 'json',
        crossDomain: true,
        headers: {
            'Access-Control-Allow-Origin': '*',
            "Accept" : "application/json"
        },
        contentType: "application/json; charset=utf-8",
        data: a,
        success: function (data) {
            if (data['message'] == "Success") {
                $('#UserActivateModal').hide();
                $('#UserActivateModal #RoleTitle').html('');
                $('#UserActivateModal #FirstName').html('');
                $('#UserActivateModal #LastName').html('');
                $('#UserActivateModal #RoleTitle').html('');
                $('#UserActivateModal #ManagerName').html('');
                $('#UserActivateModal #Username').html('');
                $('#UserActivateModal #PersonelCode').html('');
                location.reload();
            }
            else
            {
                alert(data['message']);
            }
        },
        error: function (data, xmlHttpRequest, errorText, thrownError) {
            alert(errorText);
        }
    });
}