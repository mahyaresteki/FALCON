var result = {};

$(document).on("click", ".table .fa-edit", function () {
    $('#CreateEditModal #gridSystemModalLabel').html("Edit Leave Type");
    var id = $(this).data('id');
    $("#CreateEditModal #selectedID").val(id);

    GetLeaveType(id);
    setTimeout(function(){
        $('#CreateEditModal #LeaveTypeTitle').val(result['LeaveTypeTitle']);
        $('#CreateEditModal #SalaryRatio').val(result['SalaryRatio']);
        $('#CreateEditModal #Description').val(result['Description']);
    }, 500);
});

$(document).on("click", ".table .fa-trash-alt", function () {
    var id = $(this).data('id');
    $("#DeleteModal #selectedID").val(id);

    GetLeaveType(id);
    setTimeout(function(){
        $('#DeleteModal #LeaveTypeTitle').html(result['LeaveTypeTitle']);
        $('#DeleteModal #SalaryRatio').html(result['SalaryRatio']);
        $('#DeleteModal #Description').html(result['Description']);
    }, 500);
    
    
});

$(document).on("click", ".table .fa-file-alt", function () {
    var id = $(this).data('id');
    $("#DetailModal #selectedID").val(id);

    GetLeaveType(id);
    setTimeout(function(){
        $('#DetailModal #LeaveTypeTitle').html(result['LeaveTypeTitle']);
        $('#DetailModal #SalaryRatio').html(result['SalaryRatio']);
        $('#DetailModal #Description').html(result['Description']);
    }, 500);
    
    
});

$(document).on("click", "#newLeaveType", function () {
    $('#CreateEditModal #gridSystemModalLabel').html("New Leave Type");
    $("#CreateEditModal #selectedID").val('');
    $('#CreateEditModal #LeaveTypeTitle').val('');
    $('#CreateEditModal #SalaryRatio').val('');
    $('#CreateEditModal #Description').val('');
});

$(document).on("click", "#CreateEditModal .btn-primary", function () {
    if($("#CreateEditModal #selectedID").val()=='')
    {
        CreateLeaveType($('#CreateEditModal #LeaveTypeTitle').val(), $('#CreateEditModal #SalaryRatio').val(), $('#CreateEditModal #Description').val());
    }
    else
    {
        EditLeaveType($("#CreateEditModal #selectedID").val(), $('#CreateEditModal #LeaveTypeTitle').val(), $('#CreateEditModal #SalaryRatio').val(), $('#CreateEditModal #Description').val());
    }
});

$(document).on("click", "#DeleteModal .btn-primary", function () {
    DeleteLeaveType($('#DeleteModal #selectedID').val());
});

function CreateLeaveType(leaveTypeTitle, salaryRatio, description)
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
        "LeaveTypeTitle": leaveTypeTitle,
        "SalaryRatio": salaryRatio,
        "Description": description
    };
    var a = JSON.stringify(jsondata);

    $.ajax({
        url: '/LeaveTypeManagement/CreateLeaveType',
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
                $('#CreateEditModal #LeavetTypeTitle').val('');
                $('#CreateEditModal #SalaryRatio').val('');
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

function GetLeaveType(LeaveTypeID)
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
        "LeaveTypeID": LeaveTypeID
    };
    var a = JSON.stringify(jsondata);

    $.ajax({
        url: '/LeaveTypeManagement/GetLeaveType',
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


function DeleteLeaveType(LeaveTypeID)
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
        "LeaveTypeID": LeaveTypeID
    };
    var a = JSON.stringify(jsondata);

    $.ajax({
        url: '/LeaveTypeManagement/DeleteLeaveType',
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
                $('#DeleteModal #LeaveTypeTitle').val('');
                $('#DeleteModal #SalaryRatio').val('');
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

function EditLeaveType(leaveTypeID, leaveTypeTitle, salaryRatio, description)
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
        "LeaveTypeID": leaveTypeID,
        "LeaveTypeTitle": leaveTypeTitle,
        "SalaryRatio": salaryRatio,
        "Description": description
    };
    var a = JSON.stringify(jsondata);

    $.ajax({
        url: '/LeaveTypeManagement/EditLeaveType',
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
                $('#CreateEditModal #LeaveTypeTitle').val('');
                $('#CreateEditModal #SalaryRatio').val('');
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