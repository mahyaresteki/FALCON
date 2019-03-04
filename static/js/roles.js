var result = {};

$(document).on("click", ".table .gn-icon-edit", function () {
    $('#CreateEditModal #gridSystemModalLabel').html("Edit Role");
    var id = $(this).data('id');
    $("#CreateEditModal #selectedID").val(id);

    GetRole(id);
    setTimeout(function(){
        $('#CreateEditModal #RoleTitle').val(result['RoleTitle']);
        $('#CreateEditModal #Description').val(result['Description']);
    }, 500);
});

$(document).on("click", ".table .gn-icon-delete", function () {
    var id = $(this).data('id');
    $("#DeleteModal #selectedID").val(id);

    GetRole(id);
    setTimeout(function(){
        $('#DeleteModal #RoleTitle').html(result['RoleTitle']);
        $('#DeleteModal #Description').html(result['Description']);
    }, 500);
    
    
});

$(document).on("click", ".table .gn-icon-detail", function () {
    var id = $(this).data('id');
    $("#DetailModal #selectedID").val(id);

    GetRole(id);
    setTimeout(function(){
        $('#DetailModal #RoleTitle').html(result['RoleTitle']);
        $('#DetailModal #Description').html(result['Description']);
    }, 500);
    
    
});

$(document).on("click", "#newRole", function () {
    $('#CreateEditModal #gridSystemModalLabel').html("New Role");
    $("#CreateEditModal #selectedID").val('');
    $('#CreateEditModal #RoleTitle').val('');
    $('#CreateEditModal #Description').val('');
});

$(document).on("click", "#CreateEditModal .btn-primary", function () {
    if($("#CreateEditModal #selectedID").val()=='')
    {
        CreateRole($('#CreateEditModal #RoleTitle').val(), $('#CreateEditModal #Description').val());
    }
    else
    {
        EditRole($("#CreateEditModal #selectedID").val(), $('#CreateEditModal #RoleTitle').val(), $('#CreateEditModal #Description').val());
    }
});

$(document).on("click", "#DeleteModal .btn-primary", function () {
    DeleteRole($('#DeleteModal #selectedID').val());
});

function CreateRole(roleTitle, description)
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
        "RoleTitle": roleTitle,
        "Description": description
    };
    var a = JSON.stringify(jsondata);

    $.ajax({
        url: '/UserManagement/CreateRole',
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
                $('#CreateEditModal #RoleTitle').val('');
                $('#CreateEditModal #Description').val('');
                $('#CreateEditModal #selectedID').val('');
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

function GetRole(roleID)
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
        "RoleID": roleID
    };
    var a = JSON.stringify(jsondata);

    $.ajax({
        url: '/UserManagement/GetRole',
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


function DeleteRole(roleID)
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
        "RoleID": roleID
    };
    var a = JSON.stringify(jsondata);

    $.ajax({
        url: '/UserManagement/DeleteRole',
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

function EditRole(roleId, roleTitle, description)
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
        "RoleID": roleId,
        "RoleTitle": roleTitle,
        "Description": description
    };
    var a = JSON.stringify(jsondata);

    $.ajax({
        url: '/UserManagement/EditRole',
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
                $('#CreateEditModal #RoleTitle').val('');
                $('#CreateEditModal #Description').val('');
                $('#CreateEditModal #selectedID').val('');
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