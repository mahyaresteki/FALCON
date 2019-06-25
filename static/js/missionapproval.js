$('#selectAll').on('click',function(){
    if(this.checked){
        $('.checkbox').each(function(){
            this.checked = true;
        });
    }else{
         $('.checkbox').each(function(){
            this.checked = false;
        });
    }
});

$('.checkbox').on('click',function(){
    if($('.checkbox:checked').length == $('.checkbox').length){
        $('#selectAll').prop('checked',true);
    }else{
        $('#selectAll').prop('checked',false);
    }
});


var result = {};

var osmUrl='http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
    var osmAttrib='OOPHAGA Leave Management System';
    var osm3 = new L.TileLayer(osmUrl, {attribution: osmAttrib});
    var mymap3 = new L.Map('mapid3').addLayer(osm3).setView([orglat, orglng], 18);
    var osmGeocoder3 = new L.Control.OSMGeocoder();
    mymap3.addControl(osmGeocoder3);
    var markerGroup3 = L.layerGroup().addTo(mymap3);

    var area = L.polygon(hometownArea, 
    {
        color: 'red',
        fillColor: '#f03',
        fillOpacity: 0.1
    }).addTo(mymap3);

    $(document).on("click", ".table .fa-file-alt", function () {
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

    $('#DetailModal').on('show.bs.modal', function(){
        setTimeout(function() {
            mymap3.invalidateSize();
        }, 1000);
    });


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

