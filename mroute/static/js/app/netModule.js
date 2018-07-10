/* netModule.js */

// "use strict"; TODO use strict

var netModule = (function() {

    $filter = '.row.filter-map';

    var clusterImagePath = 'https://developers.google.com/maps/documentation/javascript/examples/markerclusterer/m';

    function findNetObj(element) {
        var element_code = $(element).val();
        for (netObj of filtersArray){
            if (netObj.code == element_code) {
                return netObj;
            }
        }
    };

    function getMarkets(netObj) {
        $.get("getMarkets/", {'NET':netObj.code}, function(data){

            var markers = [];

            netObj.data_markets = JSON.parse(JSON.stringify(data));

            /* switch (true) {
                case netObj.icon_link == 'null' && netObj.icon_size_x == 'null':
                    var icon = null;
                    var icon_size = null;
                case netObj.icon_link != 'null' && netObj.icon_size_x == 'null':
                    var icon = netObj.icon_link;
                    var icon_size = null;
                case netObj.icon_link != 'null' && netObj.icon_size_x != 'null':
                    console.log(netObj);
                    var icon = netObj.icon_link;
                    var icon_size = new google.maps.Size(netObj.icon_size_x,netObj.icon_size_y);
                default:
                    var icon = null;
                    var icon_size = null;
            }; */

            for (i = 0; i < netObj.data_markets.data.length; i++) {
                var market_lat = netObj.data_markets.data[i]['market_lat'];
                var market_lng = netObj.data_markets.data[i]['market_lng'];

                marker = new google.maps.Marker({
                    position: new google.maps.LatLng(market_lat, market_lng),
                    map: map
                });

                google.maps.event.addListener(marker, 'click', (function(marker, i) {
                    var infoWindow = new google.maps.InfoWindow();
                    return function() {
                        infoWindow.setContent(netObj.data_markets.data[i]['market_net'] + ' ,' + netObj.data_markets.data[i]['market_address_ru']);
                        infoWindow.open(map, marker);
                    }
                })(marker, i));
                markers.push(marker);
            }

            if (netObj.icon_link){
                for (mk of markers) {
                    mk.setIcon({url: netObj.icon_link}); //, scaledSize: new google.maps.Size(netObj.icon_size_x,netObj.icon_size_y)});
                    // mk.icon.scaledSize = new google.maps.Size(netObj.icon_size_x, netObj.icon_size_y);
                    // mk.icon.scaledSize = new google.maps.Size(netObj.icon_size_x, netObj.icon_size_y);
                }
            }

            netObj.markerCluster = new MarkerClusterer(map, markers, {imagePath: clusterImagePath});

            netObj.markers = markers.slice();
            markers = [];
        }, "json");
    };

    function nullMarkets(netObj) {
        for (var i = 0; i < netObj.markers.length; i++) {
            netObj.markers[i].setMap(null);
        }
        netObj.markers = [];
        netObj.markerCluster.clearMarkers();
    };

    return {

        Init: function(net) {
            this.code = net[0];
            this.name = net[1];
            this.icon_link = net[2];
            this.icon_size_x = net[3];
            this.icon_size_y = net[4];
            this.data_markets = null;
            this.markers = null;
            this.markerCluster = null;
        },

        showFilterNet: function(netObj) {
            $($filter).append("<label class=\"checkbox-inline\"><input type=\"checkbox\" id=\"" + netObj.code
                              + "Checkbox\" value=\"" + netObj.code + "\" onchange=\"netModule.getNetMarkets(this)\"> "
                              + netObj.name + "<\/label>");
        },

        getNetMarkets: function(element) {

            var netObj = findNetObj(element);

            if (element.checked) {
                getMarkets(netObj);
            } else {
                nullMarkets(netObj);
            }
        }
    }
}());
