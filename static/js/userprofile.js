function ChangePassword(UserID, OldPassword, NewPassword)
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
        "OldPassword": OldPassword,
        "NewPassword": NewPassword
    };
    var a = JSON.stringify(jsondata);

    $.ajax({
        url: '/UserManagement/ChangePasswordByUser',
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