/* tableModule.js */

// "use strict"; TODO use strict

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
        var addr_val_list = [];

        $($input).each(function(indx, element){
            addr_val_list.push($(element).val());
        });

        // Find duplicate points #TODO + var!
        for (addr_val of addr_val_list) {
            var new_addr_val_list = addr_val_list.slice();
            new_addr_val_list.splice(new_addr_val_list.indexOf(addr_val), 1);
            for (new_addr_val of new_addr_val_list) {
                if (addr_val == new_addr_val) {
                    $($buttonView).prop('disabled', true);
                    // MessageModule TODO
                    $('#massage').show();
                    $('#massage').addClass("alert alert-danger").append('<p>В таблице имеются дубликаты точек!</p>');
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
                    $('#massage').addClass("alert alert-danger").append('<p>Вы должны выбрать значения во всех строках таблицы!</p>');
                    return false;
                }
            });
        }
    }
}());