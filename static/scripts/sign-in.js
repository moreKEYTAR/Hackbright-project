"use strict"; /*jslint node: true */

// default value of log-in set in route
let userChoice = $('#hidden-u-choice').data("choice");

if (userChoice == "sign-up") {
    console.log("one");
    $('#log-in-form').hide();
    $('#register-new-user-form').show();
} else {
    console.log("two");
    $('#register-new-user-form').hide();
    $('#log-in-form').show();
}
