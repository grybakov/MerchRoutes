/* routeModule.js */

"use strict";

var dayRoute = (function(){

    var day = '',
        points = '',
        calc_result = '',
        render_result = '',
        translitDict = '',
        DirectRenderObj = '';

    const DAY_PARAMS = {'Понедельник': {locator: 'pnd', stroke_color: '#98FB98'},
                       'Вторник': {locator: 'vtr', stroke_color: '#98FB98'},
                       'Среда': {locator: 'srd', stroke_color: '#87CEEB'},
                       'Четверг': {locator: 'chtv', stroke_color: '#DDA0DD'},
                       'Пятница': {locator: 'ptn', stroke_color: '#FFC0CB'},
                       'Суббота': {locator: 'sbt', stroke_color: '#4682B4'},
                       'Воскресенье': {locator: 'vskr', stroke_color: '#00CED1'}};

    function getPointsPerDay(day) {
        var pointsArray = [];
        $('input\[name=\'' + DAY_PARAMS[day].locator + '\']').each(function(i,elem) {
            if ($(this).is(':checked')) {
                var address = $(this).parent().parent().parent().find('.typeahead.form-control').text();
                pointsArray.push(address);
            }
        });
        return pointsArray;
    };

    // See more options here: https://developers.google.com/maps/documentation/javascript/reference#DirectionsRendererOptions
    // DirectionsRenderer Settings
    function getDirectionsRenderer(day) {
        var DirectionsDisplay = new google.maps.DirectionsRenderer({
            polylineOptions: {
                strokeColor: DAY_PARAMS[day].stroke_color,
                strokeWeight: 5,
                strokeOpacity: 0.85
            }
            /* markerOptions: {} */
        });
        return DirectionsDisplay;
    };

    function sayGoogle(min_time_result, day_name){
        var sourceTransArray = [],
            uniqueSourceTransArray = [],
            retranslitArray = {};

        // Header "day_name" is it results table ID
        $('.result_table_1').append('<h3>'+ day_name +'<\/h3>' +
                                    '<a href=\"javascript:\/\/\" id=\"' + day_name + '\" onclick=\"dayRoute.ViewOnMap(this)\"><button type=\"button\" class=\"btn btn-default btn-xs\"><span class=\"glyphicon glyphicon-eye-open\"><\/span> На карте!<\/button><\/a>');
        $('.result_table_1').append('<table class=\"table table-striped\" id=\"result_tb_1_'+ day_name +'\">' +
                                    '<thead class=\"thead-dark\">' +
                                    '<tr><th scope=\"col\">Начальная точка отрезка<\/th>' +
                                    '<th scope=\"col\">Конечная точка отрезка<\/th>' +
                                    '<th scope=\"col\">Расстояние, км<\/th>' +
                                    '<th scope=\"col\">Время, мин<\/th>' +
                                    '<th scope=\"col\">Время, ч<\/th><\/tr>' +
                                    '<\/thead><tbody><\/tbody><\/table>');

        // Make array for send in /marketTranslit/
        for (var sp of min_time_result['legs']){
            sourceTransArray.push(sp['start_address']);
            sourceTransArray.push(sp['end_address']);
        }

        // Delete duplicates from sourceTransArray
        $.each(sourceTransArray, function(i, el){
            if($.inArray(el, uniqueSourceTransArray) === -1) uniqueSourceTransArray.push(el);
        })

        // Save best route in bigArrayNorm[calc_result]
        for (var sr of bigArrayNorm){
            if (sr['day'] == day_name){
                sr.calc_result = min_time_result;
                continue;
            }
        }

        // Send request for translite and view result table // todo ajax
        $.post("marketTranslit/", {'data': uniqueSourceTransArray}, function(data){
            var ReadyTransArray = data['data'];
            // Сохраним словарь ReadyTransArray в translitDict объекта bigArrayNorm
            for (var tr of bigArrayNorm){
                if (tr['day'] == day_name){
                    tr.translitDict = ReadyTransArray;
                    continue;
                }
            }

            for (var good of min_time_result['legs']){
                $('#result_tb_1_'+ day_name).append('<tr><td>' + ReadyTransArray[good['start_address']] + '<\/td>' +
                                    '<td>' + ReadyTransArray[good['end_address']] + '<\/td>' +
                                    '<td>' + good['distance']['text'] + '<\/td>' +
                                    '<td>' + good['duration']['text'] + '<\/td>' +
                                    '<td>' + (good['duration']['value']/3600).toFixed(3) + '<\/td><\/tr>');
            }
            // Разблокируем кнопу генерации отчета
            $('#button_xls_report').prop('disabled', false);
            $('#button_save_report').removeClass("disabled");
        }, "json");

        // Hide loader
        // $('body').loading('stop');
    };

    function renderMap(elem, bigArrayNorm){
        var directionsService = new google.maps.DirectionsService(),
            best_route;

        // Find in bigArrayNorm day points
        for (var it of bigArrayNorm){
            if (it['day'] == elem.id){
                break;
            }
        }

        // Bind DirectRenderObj on map
        it.DirectRenderObj.setMap(map);
        if (it['render_result'] == ''){
            // If we don't have DirectionsRenderer:
            best_route = it['calc_result']
            var start_point = it['translitDict'][best_route['legs'][0]['start_address']];
            var finish_point = it['translitDict'][best_route['legs'][(best_route['legs'].length - 1)]['end_address']];

            // Make waypoints
            way_points = it['points'].slice();
            way_points.splice(way_points.indexOf(start_point), 1);
            way_points.splice(way_points.indexOf(finish_point), 1);

            // Code DirectionsWaypoint[]
            var waypts = [];
            for (f of  way_points){
                waypts.push({
                    location: f,
                    stopover: true
                });
            }

            // Make request in Directions Service
            var request = {
                origin: start_point,
                destination: finish_point,
                waypoints: waypts,
                travelMode: 'WALKING',
                unitSystem: google.maps.UnitSystem.METRIC,
                optimizeWaypoints: true};

            directionsService.route(request, function(result, status){
                if (status == 'OK'){
                    it.DirectRenderObj.setDirections(result);
                    it['render_result'] = result;
                } else {
                    messageModule.addErrorMessage('Ошибка при рендере маршрута на карте. Обратитесь к Администратору. Статус: ' + status);
                    return
                }
            });
        } else {
            // If we have DirectionsRenderer, render route
            it.DirectRenderObj.setDirections(it['render_result']);
        }
    };

    return {

        Init: function(day) {
            this.day = day;
            this.points = getPointsPerDay(day);
            this.render_result = '';
            this.DirectRenderObj = getDirectionsRenderer(day);
        },

        controlCountPoints: function(bigArray) {
            var bigArrayNorm = [];
            // Clear empty days
            for (var day of bigArray) {
                if (day['points'].length != 0) {
                    bigArrayNorm.push(day);
                }
            }
            bigArray = null;
            // Count points validation
            for (var cleared_day of bigArrayNorm) {
                if (cleared_day['points'].length < 3) {
                    messageModule.addErrorMessage('Выбранных точек должно быть не менее 3!', cleared_day['day']);
                    bigArrayNorm = null;
                    return false;
                }
            }
            return bigArrayNorm;
        },

        makeRouteAutoStart: function(bigArrayNorm) { //todo ajax
            for (var day of bigArrayNorm) {
                $.get("makeRouteAutoStart/", {'sendDay': day['day'], 'pointsArray': day['points']}, function(data){
                    // If return fail
                    if (data['status'] == 'Fail'){
                        $('body').loading('stop');
                        messageModule.addErrorMessage(data['error_massage']);
                        return
                    } else {
                        var day = data['day'];
                        var result = data['data'][0];
                        sayGoogle(result, day);
                    }
                }, "json");
            }
        },

        makeRouteFixStart: function(bigArrayNorm) { //todo ajax
            for (var day of bigArrayNorm){
                $.get("makeRouteFixStart/", {'sendDay': day['day'], 'pointsArray': day['points']}, function(data){
                    // If return fail
                    if (data['status'] == 'Fail'){
                        $('body').loading('stop');
                        messageModule.addErrorMessage(data['error_massage']);
                        return
                    } else {
                        var day = data['day'];
                        var result = data['data'][0];
                        sayGoogle(result, day);
                    }
                }, "json");
            }
        },

        ViewOnMap: function(elem) {
            // Replace icon on button
            var glaz = $(elem).find(">:first-child").find(">:first-child");

            if (glaz.hasClass('glyphicon-eye-open')){
                glaz.toggleClass('glyphicon-eye-open', false);
                glaz.toggleClass('glyphicon-eye-close');
                renderMap(elem, bigArrayNorm);
            } else {
                glaz.toggleClass('glyphicon-eye-close', false);
                glaz.toggleClass('glyphicon-eye-open');
                // Delete route on map
                for (y of bigArrayNorm){
                    if (y['day'] == elem.id){
                        y.DirectRenderObj.setMap(null);
                    }
                }
            }
        }
    }

})();