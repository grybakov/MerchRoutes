/* messageModule.js */

"use strict";

var messageModule = (function() {

    const $message = '#message',
          success_type = 'alert alert-success',
          error_type = 'alert alert-danger';


    function ErrorForDay(message, day) {
        $($message).show();
        $($message).addClass(error_type).append('<p>' + day + ': ' + message + '</p>');
    };

    function ErrorOnlyMassage(message) {
        $($message).show();
        $($message).addClass(error_type).append('<p>' + message + '</p>');
    };

    function SuccessForDay(message, day) {
        $($message).show();
        $($message).addClass(success_type).append('<p>' + day + ': ' + message + '</p>');
    };

    function SuccessOnlyMassage(message) {
        $($message).show();
        $($message).addClass(success_type).append('<p>' + message + '</p>');
    };

    return {

        addErrorMessage: function(message, day) {
            if (!day) {
                ErrorOnlyMassage(message);
            } else {
                ErrorForDay(message, day);
            }
        },

        addSuccessMessage: function(message, day) {
            if (!day) {
                SuccessOnlyMassage(message);
            } else {
                SuccessForDay(message, day);
            }
        }
    }

}());