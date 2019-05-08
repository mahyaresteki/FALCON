var result = {};

var osmUrl='http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
    var osmAttrib='OOPHAGA Leave Management System';
    var osm = new L.TileLayer(osmUrl, {attribution: osmAttrib});
    var osm2 = new L.TileLayer(osmUrl, {attribution: osmAttrib});
    var osm3 = new L.TileLayer(osmUrl, {attribution: osmAttrib});
    var mymap = new L.Map('mapid').addLayer(osm).setView([orglat, orglng], 18);
    var mymap2 = new L.Map('mapid2').addLayer(osm2).setView([orglat, orglng], 18);
    var mymap3 = new L.Map('mapid3').addLayer(osm3).setView([orglat, orglng], 18);
    var osmGeocoder = new L.Control.OSMGeocoder();
    var osmGeocoder2 = new L.Control.OSMGeocoder();
    var osmGeocoder3 = new L.Control.OSMGeocoder();
    mymap.addControl(osmGeocoder);
    mymap2.addControl(osmGeocoder2);
    mymap3.addControl(osmGeocoder3);

    var markerGroup = L.layerGroup().addTo(mymap);
    var markerGroup2 = L.layerGroup().addTo(mymap2);
    var markerGroup3 = L.layerGroup().addTo(mymap3);

    var marker = L.marker([35.73096138196363, 51.432843112140745]).addTo(markerGroup);

    mymap.addControl(osmGeocoder);

    var area = L.polygon(hometownArea, 
    {
        color: 'red',
        fillColor: '#f03',
        fillOpacity: 0.1
    }).addTo(mymap);

    function onMapClick(e) {
        var markerPoint = L.marker(e.latlng);
        if(!isMarkerInsideHometownArea(markerPoint, area))
        {
            markerGroup.clearLayers();
            var marker = L.marker(e.latlng).addTo(markerGroup);
            $('#CreateEditModal #Latitude').val(e.latlng.lat);
            $('#CreateEditModal #Longitude').val(e.latlng.lng);
        }
        else{
            alert('Your selected Location is in hometwon area. So you have to insert this mission into "Intra City Mission".');
        }

    }

    function isMarkerInsideHometownArea(marker, poly) {
        var polyPoints = poly.getLatLngs();
        var x = marker.getLatLng().lat, y = marker.getLatLng().lng;

        var inside = false;
        for (var i = 0, j = polyPoints[0].length - 1; i < polyPoints[0].length; j = i++) {
            var xi = polyPoints[0][i].lat, yi = polyPoints[0][i].lng;
            var xj = polyPoints[0][j].lat, yj = polyPoints[0][j].lng;

            var intersect = ((yi > y) != (yj > y))
                && (x < (xj - xi) * (y - yi) / (yj - yi) + xi);
            if (intersect) inside = !inside;
        }
        return inside;
    }

    mymap.on('click', onMapClick);

    $(document).on("click", ".table .gn-icon-edit", function () {
        $('#CreateEditModal #gridSystemModalLabel').html("Edit Out of City Mission");
        var id = $(this).data('id');
        $("#CreateEditModal #selectedID").val(id);

        GetMission(id);
        setTimeout(function(){
            $('#CreateEditModal #StartDate').val(result['StartDate']);
            $('#CreateEditModal #StartTime').val(result['StartTime']);
            $('#CreateEditModal #EndDate').val(result['EndDate']);
            $('#CreateEditModal #EndTime').val(result['EndTime']);
            $('#CreateEditModal #MissionTitle').val(result['MissionTitle']);
            $('#CreateEditModal #Latitude').val(result['Latitude']);
            $('#CreateEditModal #Longitude').val(result['Longitude']);
            mymap.panTo(new L.LatLng(parseFloat(result['Latitude']), parseFloat(result['Longitude'])));
            markerGroup.clearLayers();
            var marker = L.marker([parseFloat(result['Latitude']), parseFloat(result['Longitude'])]).addTo(markerGroup);
            $('#CreateEditModal #TransportTypeWentID').val(result['TransportTypeWentID']);
            $('#CreateEditModal #WentPayment').val(result['WentPayment']);
            $('#CreateEditModal #TransportTypeReturnID').val(result['TransportTypeReturnID']);
            $('#CreateEditModal #ReturnPayment').val(result['ReturnPayment']);
            $('#CreateEditModal #Description').val(result['Description']);
        }, 500);
    });

    $(document).on("click", ".table .gn-icon-delete", function () {
        var id = $(this).data('id');
        $("#DeleteModal #selectedID").val(id);

        GetMission(id);
        setTimeout(function(){
            $('#DeleteModal #StartDate').html(result['StartDate']+' '+result['StartTime']);
            $('#DeleteModal #EndDate').html(result['EndDate']+' '+result['EndTime']);
            $('#DeleteModal #MissionTitle').html(result['MissionTitle']);
            mymap2.panTo(new L.LatLng(parseFloat(result['Latitude']), parseFloat(result['Longitude'])));
            markerGroup2.clearLayers();
            var marker2 = L.marker([parseFloat(result['Latitude']), parseFloat(result['Longitude'])]).addTo(markerGroup2);
            $('#DeleteModal #TransportTypeWentTitle').html(result['TransportTypeWentTitle']);
            $('#DeleteModal #WentPayment').html(result['WentPayment']);
            $('#DeleteModal #TransportTypeReturnID').html(result['TransportTypeReturnID']);
            $('#DeleteModal #ReturnPayment').html(result['ReturnPayment']);
            $('#DeleteModal #Description').html(result['Description']);
        }, 500);
    });

    $(document).on("click", ".table .gn-icon-detail", function () {
        var id = $(this).data('id');
        $("#DetailModal #selectedID").val(id);

        GetMission(id);
        setTimeout(function(){
            $('#DetailModal #StartDate').html(result['StartDate']+' '+result['StartTime']);
            $('#DetailModal #EndDate').html(result['EndDate']+' '+result['EndTime']);
            $('#DetailModal #MissionTitle').html(result['MissionTitle']);
            mymap3.panTo(new L.LatLng(parseFloat(result['Latitude']), parseFloat(result['Longitude'])));
            markerGroup3.clearLayers();
            var marker3 = L.marker([parseFloat(result['Latitude']), parseFloat(result['Longitude'])]).addTo(markerGroup3);
            $('#DetailModal #TransportTypeWentTitle').html(result['TransportTypeWentTitle']);
            $('#DetailModal #WentPayment').html(result['WentPayment']);
            $('#DetailModal #TransportTypeReturnID').html(result['TransportTypeReturnID']);
            $('#DetailModal #ReturnPayment').html(result['ReturnPayment']);
            $('#DetailModal #Description').html(result['Description']);
        }, 500);
    });

    $(document).on("click", "#newMission", function () {
        $('#CreateEditModal #gridSystemModalLabel').html("New Out of City Mission");
        $("#CreateEditModal #selectedID").val('');
        $('#CreateEditModal #StartDate').val('');
        $('#CreateEditModal #StartTime').val('');
        $('#CreateEditModal #EndDate').val('');
        $('#CreateEditModal #EndTime').val('');
        $('#CreateEditModal #MissionTitle').val('');
        $('#CreateEditModal #Latitude').val(orglat);
        $('#CreateEditModal #Longitude').val(orglng);
        markerGroup.clearLayers();
        var marker = L.marker([orglat, orglng]).addTo(markerGroup);
        $('#CreateEditModal #TransportTypeWentID').val('');
        $('#CreateEditModal #WentPayment').val('');
        $('#CreateEditModal #TransportTypeReturnID').val('');
        $('#CreateEditModal #ReturnPayment').val('');
        $('#CreateEditModal #Description').val('');
    });

    $('#CreateEditModal').on('show.bs.modal', function(){
        setTimeout(function() {
            mymap.invalidateSize();
        }, 1000);
    });

    $('#DeleteModal').on('show.bs.modal', function(){
        setTimeout(function() {
            mymap2.invalidateSize();
        }, 1000);
    });

    $('#DetailModal').on('show.bs.modal', function(){
        setTimeout(function() {
            mymap3.invalidateSize();
        }, 1000);
    });

    $(document).on("click", "#CreateEditModal .btn-primary", function () {
        if($("#CreateEditModal #selectedID").val()=='')
        {
            CreateMission($('#CreateEditModal #StartDate').val()+' '+$('#CreateEditModal #StartTime').val(), $('#CreateEditModal #EndDate').val()+' '+$('#CreateEditModal #EndTime').val(),  $('#CreateEditModal #MissionTitle').val(), $('#CreateEditModal #Latitude').val(), $('#CreateEditModal #Longitude').val(), $('#CreateEditModal #TransportTypeWentID').val(), $('#CreateEditModal #WentPayment').val(), $('#CreateEditModal #TransportTypeReturnID').val(), $('#CreateEditModal #ReturnPayment').val());
        }
        else
        {
            EditMission($("#CreateEditModal #selectedID").val(), $('#CreateEditModal #StartDate').val()+' '+$('#CreateEditModal #StartTime').val(), $('#CreateEditModal #EndDate').val()+' '+$('#CreateEditModal #EndTime').val(), $('#CreateEditModal #MissionTitle').val(), $('#CreateEditModal #Latitude').val(), $('#CreateEditModal #Longitude').val(), $('#CreateEditModal #TransportTypeWentID').val(), $('#CreateEditModal #WentPayment').val(), $('#CreateEditModal #TransportTypeReturnID').val(), $('#CreateEditModal #ReturnPayment').val());
        }
    });

    $(document).on("click", "#DeleteModal .btn-primary", function () {
        DeleteMission($('#DeleteModal #selectedID').val());
    });

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
        "ReturnPayment": ReturnPayment,
        "IsIntraCityMission": 'False'
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