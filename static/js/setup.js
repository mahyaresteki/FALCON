function setDatabase(host, database,username, password) {
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
        "host": host,
        "database": database,
        "username": username,
        "password": password
    };
    var a = JSON.stringify(jsondata);

    $.ajax({
        url: '/Home/SetDatabase',
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
                $('#setDatabase').hide();
                $('#setAdministrator').show();
            }
            else
            {
                $("#Error").text(data['message']);
            }
        },
        error: function (data, xmlHttpRequest, errorText, thrownError) {
            $(".modal1").hide();
            $("#errorPanel").show();
            $("#Error").text(errorText);
        }
    });
}


function setAdministrator(firstname, lastname,username, password, personelcode) {
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
        "FirstName": firstname,
        "LastName": lastname,
        "Username": username,
        "Password": password,
        "PersonelCode":personelcode
    };
    var a = JSON.stringify(jsondata);

    $.ajax({
        url: '/Home/SetAdministrator',
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
                window.location.href = '/';
            }
            else
            {
                $("#Error").text(data['message']);
            }
        },
        error: function (data, xmlHttpRequest, errorText, thrownError) {
            $(".modal1").hide();
            $("#errorPanel").show();
            $("#Error").text(errorText);
        }
    });
}
