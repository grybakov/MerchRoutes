/* tableModule.js */

"use strict";

var tableModule = (function() {

    const GET_ALL_MARKETS_URL = 'getAllMarkets/';
    const maxRows = 25;

    const $table = '#route_table';
    const $input = '.typeahead.form-control';

    function getAllMarkets() {
        $.get(GET_ALL_MARKETS_URL, function(data){
            $($input).typeahead({source: data,
                              minLength: 1,
                              items: 10,
                              autoSelect: true,
                              afterSelect: function(item) {controlDuplicate(item)}
            });
        }, 'json');
    };

    function controlButtonView() {
        if (tableModule.getRowCount() >= 3) {
            $($buttonView).prop('disabled', false);
        } else {
            $($buttonView).prop('disabled', true);
        }
    };

    function controlMaxRows() {
        if (maxRows != 0 && tableModule.getRowCount() >= maxRows) {
            $($buttonView).prop('disabled', true);
            $($buttonAdd).prop('disabled', true);
        } else {
            $($buttonView).prop('disabled', false);
        }
    };

    function controlDuplicate(item) {
        // Get address
        var addr_list = [];

        $($input).each(function(indx, element){
            addr_list.push($(element).val());
        });

        // Find duplicate points
        for (var addr of addr_list) {
            var new_addr_list = addr_list.slice();
            new_addr_list.splice(new_addr_list.indexOf(addr), 1);
            for (var new_addr of new_addr_list) {
                if (addr == new_addr) {
                    $($buttonView).prop('disabled', true);
                    messageModule.addErrorMessage('В таблице имеются дубликаты точек! Так быть не должно.');
                    break;
                }
            }
        }
         // Block input #TODO
        $('.typeahead').prop('disabled', true);
        return item;
    };

    return {

        addRow: function() {
            $($table).append("<tr><td><a href=\"javascript:\/\/\" onclick=\"tableModule.moveRowUp(this)\"><span class=\"glyphicon glyphicon-arrow-up\"></span><\/a><\/td>" +
                            "<td><a href=\"javascript:\/\/\" onclick=\"tableModule.moveRowDown(this)\"><span class=\"glyphicon glyphicon-arrow-down\"></span><\/a><\/td>" +
                            "<td><input type=\"text\" class=\"typeahead form-control\" data-provide=\"typeahead\"><\/td>" +
                            "<td><a href=\"javascript:\/\/\" onclick=\"tableModule.deleteRow(this)\"><span class=\"glyphicon glyphicon-remove\"></span></a><\/td>" +
                            "<td><div class=\"checkbox\"><input type=\"checkbox\" id=\"pnd\" name=\"pnd\"><\/div><\/td>" +
                            "<td><div class=\"checkbox\"><input type=\"checkbox\" id=\"vtr\" name=\"vtr\"><\/div><\/td>" +
                            "<td><div class=\"checkbox\"><input type=\"checkbox\" id=\"srd\" name=\"srd\"><\/div><\/td>" +
                            "<td><div class=\"checkbox\"><input type=\"checkbox\" id=\"chtv\" name=\"chtv\"><\/div><\/td>" +
                            "<td><div class=\"checkbox\"><input type=\"checkbox\" id=\"ptn\" name=\"ptn\"><\/div><\/td>" +
                            "<td><div class=\"checkbox\"><input type=\"checkbox\" id=\"sbt\" name=\"sbt\"><\/div><\/td>" +
                            "<td><div class=\"checkbox\"><input type=\"checkbox\" id=\"vskr\" name=\"vskr\"><\/div><\/td><\/tr>");
            controlMaxRows();
            controlButtonView();
            getAllMarkets();
        },

        deleteRow: function(element) {
            $(element).parent().parent().remove();
            clearElementsResult();
            controlMaxRows();
            controlButtonView();
        },

        moveRowUp: function(element) {
            var row = $(element).parents("tr");
            row.insertBefore(row.prev());
        },

        moveRowDown: function(element) {
            var row = $(element).parents("tr");
            row.insertAfter(row.next());
        },

        getRowCount: function() {
            return $($input).length;
        },

        controlEmptyInput: function() {
            $($input).each(function(index, element){
                // TODO cut == '' ?
                if ($(element).val() == '') {
                    messageModule.addErrorMessage('Вы должны выбрать значения во всех строках таблицы!');
                    return;
                }
            });
        }
    }
}());