var result = {};

$(document).on("click", ".table .gn-icon-edit", function () {
    $('#CreateEditModal #gridSystemModalLabel').html("Edit Transport Type");
    var id = $(this).data('id');
    $("#CreateEditModal #selectedID").val(id);

    GetTransportType(id);
    setTimeout(function(){
        $('#CreateEditModal #TransportTypeTitle').val(result['TransportTypeTitle']);
        $('#CreateEditModal #Description').val(result['Description']);
    }, 500);
});

$(document).on("click", ".table .gn-icon-delete", function () {
    var id = $(this).data('id');
    $("#DeleteModal #selectedID").val(id);

    GetTransportType(id);
    setTimeout(function(){
        $('#DeleteModal #TransportTypeTitle').html(result['TransportTypeTitle']);
        $('#DeleteModal #Description').html(result['Description']);
    }, 500);
    
    
});

$(document).on("click", ".table .gn-icon-detail", function () {
    var id = $(this).data('id');
    $("#DetailModal #selectedID").val(id);

    GetTransportType(id);
    setTimeout(function(){
        $('#DetailModal #TransportTypeTitle').html(result['TransportTypeTitle']);
        $('#DetailModal #Description').html(result['Description']);
    }, 500);
    
    
});

$(document).on("click", "#newTransportType", function () {
    $('#CreateEditModal #gridSystemModalLabel').html("New Transport Type");
    $("#CreateEditModal #selectedID").val('');
    $('#CreateEditModal #TransportTypeTitle').val('');
    $('#CreateEditModal #Description').val('');
});

$(document).on("click", "#CreateEditModal .btn-primary", function () {
    if($("#CreateEditModal #selectedID").val()=='')
    {
        CreateTransportType($('#CreateEditModal #TransportTypeTitle').val(), $('#CreateEditModal #Description').val());
    }
    else
    {
        EditTransportType($("#CreateEditModal #selectedID").val(), $('#CreateEditModal #TransportTypeTitle').val(), $('#CreateEditModal #Description').val());
    }
});

$(document).on("click", "#DeleteModal .btn-primary", function () {
    DeleteTransportType($('#DeleteModal #selectedID').val());
});

function CreateTransportType(transportTypeTitle, description)
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
        "TransportTypeTitle": transportTypeTitle,
        "Description": description
    };
    var a = JSON.stringify(jsondata);

    $.ajax({
        url: '/TransportTypeManagement/CreateTransportType',
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
                $('#CreateEditModal #TransportTypeTitle').val('');
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

function GetTransportType(TransportTypeID)
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
        "TransportTypeID": TransportTypeID
    };
    var a = JSON.stringify(jsondata);

    $.ajax({
        url: '/TransportTypeManagement/GetTransportType',
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


function DeleteTransportType(TransportTypeID)
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
        "TransportTypeID": TransportTypeID
    };
    var a = JSON.stringify(jsondata);

    $.ajax({
        url: '/TransportTypeManagement/DeleteTransportType',
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
                $('#DeleteModal #TransportTypeTitle').val('');
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

function EditTransportType(TransportTypeID, TransportTypeTitle, description)
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
        "TransportTypeID": TransportTypeID,
        "TransportTypeTitle": TransportTypeTitle,
        "Description": description
    };
    var a = JSON.stringify(jsondata);

    $.ajax({
        url: '/TransportTypeManagement/EditTransportType',
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
                $('#CreateEditModal #TransportTypeTitle').val('');
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