/* Map Settings */

function initMap() {
    $('#button_view').prop('disabled', true);
    $('#button_xls_report').prop('disabled', true);
    $('#button_save_report').addClass("disabled");

    map = new google.maps.Map(document.getElementById('map'), {
        zoom: 10,
        center: {lat: 55.740911, lng: 37.654136},
    });
}