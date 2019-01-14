var result = {};

function CreateUser(FirstName, LastName, Username, Password, RoleID, PersonelCode)
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
        "PersonelCode": PersonelCode
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
                $('#DeleteModal #RoleTitle').val('');
                $('#DeleteModal #Description').val('');
                $('#DeleteModal #selectedID').val('');
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

function EditUser(UserID, FirstName, LastName, Username, RoleID, PersonelCode)
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
        "PersonelCode": PersonelCode
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