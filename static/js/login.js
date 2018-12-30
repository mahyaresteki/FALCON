$(document).ready(function () {
    $(".modal1").hide();
});

$('body').keypress(function (e) {
    if (e.keyCode == '13') {
        $(this).find('#btnLogin').click();
    }
});



function LogIn(username, password) {
    if (username != '' && password != '') {
        $(".modal1").show();

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
            "username": username,
            "password": password
        };
        var a = JSON.stringify(jsondata);

        $.ajax({
            url: '/Home/Login',
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
                    window.location.href = '/Dashboard';
                }
                else
                {
                    $(".modal1").hide();
                    $("#errorPanel").show();
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
    else {
        $("#Error").text('Please insert username and password.');
    }
}