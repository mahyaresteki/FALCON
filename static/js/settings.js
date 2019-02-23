function SaveSettings(ServerIP, Port, Host, Database, User, Password, OrganizationName, Latitude, Longitude)
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
        "Server": ServerIP,
        "Port": Port,
        "Host": Host,
        "Database": Database,
        "User": User,
        "Password": Password,
        "OrganizationName": OrganizationName,
        "Latitude": Latitude,
        "Longitude": Longitude
    };
    var a = JSON.stringify(jsondata);

    $.ajax({
        url: '/SettingsManagement/SaveSettings',
        type: 'POST',
        dataType: 'json',
        crossDomain: true,
        timeout: 3000,
        headers: {
            'Access-Control-Allow-Origin': '*',
            "Accept" : "application/json"
        },
        contentType: "application/json; charset=utf-8",
        data: a,
        success: function (data) {
        },
        error: function (data, xmlHttpRequest, errorText, thrownError) {
        }
    });
}