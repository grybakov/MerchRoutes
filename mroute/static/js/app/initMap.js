/* Map & DirectionsRenderer Settings */

function initMap() {

    $('#button_view').prop('disabled', true);
    $('#button_xls_report').prop('disabled', true);
    $('#button_save_report').addClass("disabled");

    // see more options here: https://developers.google.com/maps/documentation/javascript/reference#DirectionsRendererOptions
    // DirectionsRenderer Settings
    DirectionsRendererArray = []
    var strokeColorArray = ['#98FB98', '#98FB98', '#87CEEB', '#DDA0DD', '#FFC0CB', '#4682B4', '#00CED1'];

    for (i = 0; i < strokeColorArray.length; i++){
        var DirectionsDisplay = new google.maps.DirectionsRenderer({
            polylineOptions: {
                strokeColor: strokeColorArray[i],
                strokeWeight: 5,
                strokeOpacity: 0.85
            }
            // markerOptions: {
            // Задел на будущее
            // }
        });
        DirectionsRendererArray.push(DirectionsDisplay);
    }

    map = new google.maps.Map(document.getElementById('map'), {
        zoom: 10,
        center: {lat: 55.740911, lng: 37.654136},
    });
}