$(function(){
    $( "#accordion" ).accordion({ heightStyle: "content"});
});
$(document).on("click", "#btnSave", function () {
    SaveSettings($('#Server').val(), $('#Port').val(), $('#Host').val(), $('#Database').val(), $('#User').val(), $('#Password').val(), $('#OrganizationName').val(), $('#Latitude').val(), $('#Longitude').val(),hometownArea);
    setTimeout(function() {
        open('http://'+$('#Server').val()+':'+$('#Port').val()+'/SettingsManagement/Settings', '_self');
    }, 2000);
});

var osmUrl='http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
var osmAttrib='OOPHAGA Leave Management System';
var osm = new L.TileLayer(osmUrl, {attribution: osmAttrib});
var mymap = new L.Map('mapid').addLayer(osm).setView([parseFloat($('#Latitude').val()), parseFloat($('#Longitude').val())], 18);
var osmGeocoder = new L.Control.OSMGeocoder();
var markerGroup = L.layerGroup().addTo(mymap);
mymap.panTo(new L.LatLng(parseFloat($('#Latitude').val()), parseFloat($('#Longitude').val())));
markerGroup.clearLayers();
var marker = L.marker([parseFloat($('#Latitude').val()), parseFloat($('#Longitude').val())]).addTo(markerGroup);

function onMapClick(e) {
    markerGroup.clearLayers();
    var marker = L.marker(e.latlng).addTo(markerGroup);
    $('#Latitude').val(e.latlng.lat);
    $('#Longitude').val(e.latlng.lng);
}

mymap.on('click', onMapClick);


var osm2 = new L.TileLayer(osmUrl, {attribution: osmAttrib});
var mymap2 = new L.Map('mapid2').addLayer(osm2).setView([parseFloat($('#Latitude').val()), parseFloat($('#Longitude').val())], 10);
var osmGeocoder2 = new L.Control.OSMGeocoder();

mymap2.addControl(osmGeocoder2);
var markerGroup2 = L.layerGroup().addTo(mymap2);



var area = L.polygon(hometownArea, 
{
    color: 'red',
    fillColor: '#f03',
    fillOpacity: 0.1
}).addTo(markerGroup2);

function onMapClick2(e) {
    markerGroup2.clearLayers();
    hometownArea.push([e.latlng.lat, e.latlng.lng]);
    var area = L.polygon(hometownArea, 
    {
        color: 'red',
        fillColor: '#f03',
        fillOpacity: 0.1
    }).addTo(markerGroup2);
}

mymap2.on('click', onMapClick2);

$(document).on("click", "#btnClearHomeTownArea", function () {
    markerGroup2.clearLayers();
    hometownArea = [];
});

function SaveSettings(ServerIP, Port, Host, Database, User, Password, OrganizationName, Latitude, Longitude, hometownArea)
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
        "Longitude": Longitude,
        "hometownArea": hometownArea
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