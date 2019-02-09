var result = {};

function CreateMission(StartDate, EndDate, MissionTitle, Latitude, Longitude, TransportTypeWentID, WentPayment, TransportTypeReturnID, ReturnPayment)
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
        "MissionTitle": MissionTitle,
        "Latitude": Latitude,
        "Longitude": Longitude,
        "TransportTypeWentID": TransportTypeWentID,
        "WentPayment": WentPayment,
        "TransportTypeReturnID": TransportTypeReturnID,
        "ReturnPayment": ReturnPayment
    };
    var a = JSON.stringify(jsondata);

    $.ajax({
        url: '/MissionManagement/CreateMission',
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
                $('#CreateEditModal #MissionTitle').val('');
                $('#CreateEditModal #Latitude').val('');
                $('#CreateEditModal #Longitude').val('');
                $('#CreateEditModal #TransportTypeWentID').val('');
                $('#CreateEditModal #WentPayment').val('');
                $('#CreateEditModal #TransportTypeReturnID').val('');
                $('#CreateEditModal #ReturnPayment').val('');
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

function GetMission(MissionID)
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
        "MissionID": MissionID
    };
    var a = JSON.stringify(jsondata);

    $.ajax({
        url: '/MissionManagement/GetMission',
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
            console.log(result);
        },
        error: function (data, xmlHttpRequest, errorText, thrownError) {
            result = errorText;
        }
    });
}


function DeleteMission(MissionID)
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
        "MissionID": MissionID
    };
    var a = JSON.stringify(jsondata);

    $.ajax({
        url: '/MissionManagement/DeleteMission',
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
                $('#DeleteModal #MissionTitle').html('');
                $('#DeleteModal #Latitude').val('');
                $('#DeleteModal #Longitude').val('');
                $('#DeleteModal #TransportTypeWentTitle').html('');
                $('#DeleteModal #WentPayment').html('');
                $('#DeleteModal #TransportTypeReturnTitle').html('');
                $('#DeleteModal #ReturnPayment').html('');
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

function EditMission(MissionID, StartDate, EndDate, MissionTitle, Latitude, Longitude, TransportTypeWentID, WentPayment, TransportTypeReturnID, ReturnPayment)
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
        "MissionID": MissionID,
        "StartDate": StartDate,
        "EndDate": EndDate,
        "MissionTitle": MissionTitle,
        "Latitude": Latitude,
        "Longitude": Longitude,
        "TransportTypeWentID": TransportTypeWentID,
        "WentPayment": WentPayment,
        "TransportTypeReturnID": TransportTypeReturnID,
        "ReturnPayment": ReturnPayment
    };
    var a = JSON.stringify(jsondata);

    $.ajax({
        url: '/MissionManagement/EditMission',
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
                $('#CreateEditModal #MissionTitle').val('');
                $('#CreateEditModal #Latitude').val('');
                $('#CreateEditModal #Longitude').val('');
                $('#CreateEditModal #TransportTypeWentID').val('');
                $('#CreateEditModal #WentPayment').val('');
                $('#CreateEditModal #TransportTypeReturnID').val('');
                $('#CreateEditModal #ReturnPayment').val('');
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