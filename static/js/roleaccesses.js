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
                table+='<tr><td>'+data[i][3]+'</td><td><input type="checkbox" data-role-id="'+data[i][0]+'" data-form-id="'+data[i][2]+'" data-grant="create" '+(data[i][4]==true?'checked':'')+' /></td><td><input type="checkbox" data-role-id="'+data[i][0]+'" data-form-id="'+data[i][2]+'" data-grant="read" '+(data[i][5]==true?'checked':'')+' /></td><td><input type="checkbox" data-role-id="'+data[i][0]+'" data-form-id="'+data[i][2]+'" data-grant="update" '+(data[i][6]==true?'checked':'')+' /></td><td><input type="checkbox" data-role-id="'+data[i][0]+'" data-form-id="'+data[i][2]+'" data-grant="delete" '+(data[i][7]==true?'checked':'')+' /></td><td><input type="checkbox" data-role-id="'+data[i][0]+'" data-form-id="'+data[i][2]+'" data-grant="print" '+(data[i][8]==true?'checked':'')+' /></td></tr>';
            }
            $('.table').html(table);
        },
        error: function (data, xmlHttpRequest, errorText, thrownError) {
            result = errorText;
        }
    });
}


function SaveAccesses(){
    var accesses = [];
    $(".table input:checkbox").each(function() {
        accesses.push(
            {roleId: $(this).attr("data-role-id"), fromId: $(this).attr("data-form-id"), grant: $(this).attr("data-grant"), value: $(this).prop("checked")}
        );
    });
    console.log(accesses);

}