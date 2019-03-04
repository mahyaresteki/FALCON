var result = {};

$(document).on("click", ".table .gn-icon-edit", function () {
    $('#CreateEditModal #gridSystemModalLabel').html("Edit User");
    var id = $(this).data('id');
    $("#CreateEditModal #selectedID").val(id);

    GetUser(id);
    setTimeout(function(){
        $("#CreateEditModal #selectedID").val(id);
        $('#CreateEditModal #FirstName').val(result['FirstName']);
        $('#CreateEditModal #LastName').val(result['LastName']);
        $('#CreateEditModal #PersonelCode').val(result['PersonelCode']);
        $("#CreateEditModal #Username").val(result['Username']);
        $("#CreateEditModal #RoleID").val(result['RoleID']);
        $("#CreateEditModal #ManagerID").val(result['ManagerID']);
        $('#CreateEditModal #PasswordBox1').hide();
        $('#CreateEditModal #PasswordBox2').hide();
    }, 700);
});

$(document).on("click", ".table .gn-icon-user-activate, .gn-icon-user-deactivate", function () {
    var id = $(this).data('id');
    $("#UserActivateModal #selectedID").val(id);
    GetUser(id);
    setTimeout(function(){
        $("#UserActivateModal #selectedID").val(id);
        $('#UserActivateModal #FirstName').html(result['FirstName']);
        $('#UserActivateModal #LastName').html(result['LastName']);
        $('#UserActivateModal #PersonelCode').html(result['PersonelCode']);
        $("#UserActivateModal #Username").html(result['Username']);
        $("#UserActivateModal #RoleTitle").html(result['RoleTitle']);
        $("#UserActivateModal #IsActive").html(result['IsActive']);
        $("#UserActivateModal #ManagerName").html(result['ManagerName']);

    }, 700);
});

$(document).on("click", ".table .gn-icon-change-password", function () {
    var id = $(this).data('id');
    $("#ChangePasswordModal #selectedID").val(id);
});

$(document).on("click", ".table .gn-icon-delete", function () {
    var id = $(this).data('id');
    $("#DeleteModal #selectedID").val(id);

    GetUser(id);
    setTimeout(function(){
        $("#DeleteModal #selectedID").val(id);
        $('#DeleteModal #FirstName').html(result['FirstName']);
        $('#DeleteModal #LastName').html(result['LastName']);
        $('#DeleteModal #PersonelCode').html(result['PersonelCode']);
        $("#DeleteModal #Username").html(result['Username']);
        $('#DeleteModal #RoleTitle').html(result['RoleTitle']);
        $("#DeleteModal #ManagerName").html(result['ManagerName']);
    }, 700);
    
    
});

$(document).on("click", ".table .gn-icon-detail", function () {
    var id = $(this).data('id');
    $("#DetailModal #selectedID").val(id);

    GetUser(id);
    setTimeout(function(){
        $("#DetailModal #selectedID").val(id);
        $('#DetailModal #FirstName').html(result['FirstName']);
        $('#DetailModal #LastName').html(result['LastName']);
        $('#DetailModal #PersonelCode').html(result['PersonelCode']);
        $("#DetailModal #Username").html(result['Username']);
        $('#DetailModal #RoleTitle').html(result['RoleTitle']);
        $("#DetailModal #ManagerName").html(result['ManagerName']);
    }, 700);
    
    
});

$(document).on("click", "#newUser", function () {
    $('#CreateEditModal #gridSystemModalLabel').html("New User");
    $("#CreateEditModal #selectedID").val('');
    $('#CreateEditModal #FirstName').val('');
    $('#CreateEditModal #LastName').val('');
    $('#CreateEditModal #PersonelCode').val('');
    $("#CreateEditModal #Username").val('');
    $("#CreateEditModal #Password").val('');
    $('#CreateEditModal #RoleID').val('');
    $('#CreateEditModal #ManagerID').val('');
    $('#CreateEditModal #PersonelCode').val('');
    $('#CreateEditModal #PasswordBox1').show();
    $('#CreateEditModal #PasswordBox2').show();
});

$(document).on("click", "#CreateEditModal .btn-primary", function () {
    if($("#CreateEditModal #selectedID").val()=='')
    {
        CreateUser($('#CreateEditModal #FirstName').val(), $('#CreateEditModal #LastName').val() , $('#CreateEditModal #Username').val(), $('#CreateEditModal #Password').val(), $('#CreateEditModal #RoleID').val(), $('#CreateEditModal #PersonelCode').val(), $('#CreateEditModal #ManagerID').val());
    }
    else
    {
        EditUser($("#CreateEditModal #selectedID").val(), $('#CreateEditModal #FirstName').val(), $('#CreateEditModal #LastName').val() , $('#CreateEditModal #Username').val(), $('#CreateEditModal #RoleID').val(), $('#CreateEditModal #PersonelCode').val(), $('#CreateEditModal #ManagerID').val());
    }
});

$(document).on("click", "#DeleteModal .btn-primary", function () {
    DeleteUser($('#DeleteModal #selectedID').val());
});

$(document).on("click", "#UserActivateModal .btn-primary", function () {
    UserActivate($('#UserActivateModal #selectedID').val());
});

$(document).on("click", "#ChangePasswordModal .btn-primary", function () {
    ChangePassword($('#ChangePasswordModal #selectedID').val(), $('#ChangePasswordModal #Password').val());
});

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