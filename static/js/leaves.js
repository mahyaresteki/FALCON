var result = {};

$(document).on("click", ".table .fa-edit", function () {
    $('#CreateEditModal #gridSystemModalLabel').html("Edit Leave");
    var id = $(this).data('id');
    $("#CreateEditModal #selectedID").val(id);

    GetLeave(id);
    setTimeout(function(){
        $('#CreateEditModal #StartDate').val(result['StartDate']);
        $('#CreateEditModal #StartTime').val(result['StartTime']);
        $('#CreateEditModal #EndDate').val(result['EndDate']);
        $('#CreateEditModal #EndTime').val(result['EndTime']);
        $('#CreateEditModal #Reason').val(result['Reason']);
        $('#CreateEditModal #Description').val(result['Description']);
    }, 500);
});

$(document).on("click", ".table .fa-trash-alt", function () {
    var id = $(this).data('id');
    $("#DeleteModal #selectedID").val(id);

    GetLeave(id);
    setTimeout(function(){
        $('#DeleteModal #StartDate').html(result['StartDate']+' '+result['StartTime']);
        $('#DeleteModal #EndDate').html(result['EndDate']+' '+result['EndTime']);
        $('#DeleteModal #Reason').html(result['Reason']);
    }, 500);
});

$(document).on("click", ".table .fa-file-alt", function () {
    var id = $(this).data('id');
    $("#DetailModal #selectedID").val(id);

    GetLeave(id);
    setTimeout(function(){
        $('#DetailModal #StartDate').html(result['StartDate']+' '+result['StartTime']);
        $('#DetailModal #EndDate').html(result['EndDate']+' '+result['EndTime']);
        $('#DetailModal #Reason').html(result['Reason']);
    }, 500);
});

$(document).on("click", "#newLeave", function () {
    $('#CreateEditModal #gridSystemModalLabel').html("New Leave");
    $("#CreateEditModal #selectedID").val('');
    $('#CreateEditModal #StartDate').val('');
    $('#CreateEditModal #StartTime').val('');
    $('#CreateEditModal #EndDate').val('');
    $('#CreateEditModal #EndTime').val('');
    $('#CreateEditModal #Reason').val('');
});

$(document).on("click", "#CreateEditModal .btn-primary", function () {
    if($("#CreateEditModal #selectedID").val()=='')
    {
        CreateLeave($('#CreateEditModal #StartDate').val()+' '+$('#CreateEditModal #StartTime').val(), $('#CreateEditModal #EndDate').val()+' '+$('#CreateEditModal #EndTime').val(),  $('#CreateEditModal #Reason').val());
    }
    else
    {
        EditLeave($("#CreateEditModal #selectedID").val(), $('#CreateEditModal #StartDate').val()+' '+$('#CreateEditModal #StartTime').val(), $('#CreateEditModal #EndDate').val()+' '+$('#CreateEditModal #EndTime').val(),  $('#CreateEditModal #Reason').val());
    }
});

$(document).on("click", "#DeleteModal .btn-primary", function () {
    DeleteLeave($('#DeleteModal #selectedID').val());
});

function CreateLeave(StartDate, EndDate, Reason)
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
        "StartDate": StartDate,
        "EndDate": EndDate,
        "Reason": Reason
    };
    var a = JSON.stringify(jsondata);

    $.ajax({
        url: '/LeaveManagement/CreateLeave',
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
                $('#CreateEditModal #StartDate').val('');
                $('#CreateEditModal #StartTime').val('');
                $('#CreateEditModal #EndDate').val('');
                $('#CreateEditModal #EndTime').val('');
                $('#CreateEditModal #Reason').val('');
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

function GetLeave(LeaveID)
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
        "LeaveID": LeaveID
    };
    var a = JSON.stringify(jsondata);

    $.ajax({
        url: '/LeaveManagement/GetLeave',
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


function DeleteLeave(LeaveID)
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
        "LeaveID": LeaveID
    };
    var a = JSON.stringify(jsondata);

    $.ajax({
        url: '/LeaveManagement/DeleteLeave',
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
                $('#DeleteModal #StartDate').html('');
                $('#DeleteModal #EndDate').html('');
                $('#DeleteModal #Reason').html('');
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

function EditLeave(LeaveID,StartDate, EndDate, Reason)
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
        "LeaveID": LeaveID,
        "StartDate": StartDate,
        "EndDate": EndDate,
        "Reason": Reason
    };
    var a = JSON.stringify(jsondata);

    $.ajax({
        url: '/LeaveManagement/EditLeave',
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
                $('#CreateEditModal #StartDate').val('');
                $('#CreateEditModal #EndDate').val('');
                $('#CreateEditModal #StartTime').val('');
                $('#CreateEditModal #EndTime').val('');
                $('#CreateEditModal #Reason').val('');
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