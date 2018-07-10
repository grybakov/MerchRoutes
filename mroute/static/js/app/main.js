/* MerchRoutes - main.js */

// 'use strict';

$(window).load(
    function(){

        var map;
        window.$buttonView = '#button_view',
        window.$buttonAdd = '#button_add',
        window.$buttonSave = '#button_save_route',
        window.$buttonXlsReport = '#button_xls_report',
        window.$filter = '.row.filter-map',
        window.filtersArray = [],
        window.bigArrayNorm = [];

        initMap();
        getFilterNets();

        $($buttonView).click(
            function(){
                var bigArray = [],
                    dayArray = ['Понедельник','Вторник','Среда','Четверг','Пятница','Суббота','Воскресенье'];

                clearElementsResult();
                tableModule.controlEmptyInput();

                for (var i = 0; i <= 6; i++){
                    var day = new dayRoute.Init(dayArray[i]);
                    bigArray.push(day);
                }

                bigArrayNorm = dayRoute.controlCountPoints(bigArray);

                // Show loader!!!!!!!!!!!!!
                // $('body').loading({message:'Подождите, пожалуйста, немного..'});

                // Request to backend
                if ($('#RouteCheck').is(':checked')) {
                    dayRoute.makeRouteAutoStart(bigArrayNorm);
                } else {
                    dayRoute.makeRouteFixStart(bigArrayNorm);
                }
            }
        );

        // Add Row in table
        $($buttonAdd).click(
            function(){
                tableModule.addRow();
            }
        );

        // Save route in DB
        $($buttonSave).click(
            function(){
                var dataArray = {'name_route': $("#id_route_name").val(), 'desc_route': $("#id_route_desc").val(), 'rawArray': bigArrayNorm};
                $('#SaveModal1').modal('hide');
                $.post("SaveRoute/", CircularJSON.stringify(dataArray), function(data){
                    $('#massage').show();
                    $('#massage').addClass("alert alert-success").append('<p>' + data['data'] + '</p>');
                }, "json");
            }
        );

        // Export route in *.xls
        $($buttonXlsReport).click(
            function() {
                $.ajax({type: 'POST',
                contentType: 'application/json',
                url: 'makeXlsReport/',
                data: CircularJSON.stringify(bigArrayNorm),
                success: function(data) {
                    window.open('data:application/vnd.ms-excel;base64,'+data, '_blank');
                }
            });
        });
    });

function clearElementsResult() {
    // Delete routes from the map
    for (var mk of bigArrayNorm){
        mk.DirectRenderObj.setMap(null);
    }
    // Delete massages
    $('.alert').empty().hide();
    // Clear result_table_1 div
    $("div.result_table_1").empty()
    // Disabled buttons
    $($buttonXlsReport).prop('disabled', true);
    $('#button_save_report').addClass('disabled');
};

function getFilterNets() {
    $.ajax({
        type: 'POST',
        contentType: 'application/json',
        url: 'getNets/',
        success: function(data) {
            if (data['status'] == 'OK') {
                for (var net of data['data']) {
                    var filter = new netModule.Init(net);
                    netModule.showFilterNet(filter);
                    filtersArray.push(filter);
                }
            } else {
                // TODO error massage
            }
        },
        error: function(data) {
            // TODO error massage
        }
    })
};
