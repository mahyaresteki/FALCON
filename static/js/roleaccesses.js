function GetRoleAccesses(roleID)
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
        url: '/UserManagement/GetRoleAccesses',
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
            var table = '<tr><th>FormTitle</th><th>Create</th><th>Read</th><th>Update</th><th>Delete</th><th>Print</th></tr>';
            for (var i = 0; i < data.length; i++) {
                console.log(data[i]);
                table+='<tr><td>'+data[i][3]+'</td><td><input type="checkbox" '+(data[i][4]==true?'checked':'')+' /></td><td><input type="checkbox" '+(data[i][5]==true?'checked':'')+' /></td><td><input type="checkbox" '+(data[i][6]==true?'checked':'')+' /></td><td><input type="checkbox" '+(data[i][7]==true?'checked':'')+' /></td><td><input type="checkbox" '+(data[i][8]==true?'checked':'')+' /></td></tr>';
            }
            $('.table').html(table);
            console.log(data);
        },
        error: function (data, xmlHttpRequest, errorText, thrownError) {
            result = errorText;
        }
    });
}