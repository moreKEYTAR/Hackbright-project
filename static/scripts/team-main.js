"use strict"; /*jslint node: true */


/////////////////////////////////////////////////////////////////////////////
/// BOARD VIEW CODE ///
/////////////////////////////////////////////////////////////////////////////

// div with id all-board-projects starts with 'hidden' toggled on
$('.board-button').on('click', function (evt) {
    let boardId = $(this).data("boardId");

    // checks only the first div; if visible, toggles both off for the board
        // when the button is clicked (again)
    if ($("#show-projects-" + boardId).is(':visible')) {
        $(".show-projects").hide();  // Close the div with the projects
        $(".make-new-project").hide();  // Close the new project div
    // handles clicking another board, which is not yet visible (regardless if
        // any are visible)
    } else { 
        $(".show-projects").hide();
        $(".make-new-project").hide();
        $("#show-projects-" + boardId).show();
        $("#make-new-project-" + boardId).show();
    }
});


/////////////////////////////////////////////////////////////////////////////
/// MODAL CODE: NEW BOARD MODAL ///
/////////////////////////////////////////////////////////////////////////////

// https://www.w3schools.com/howto/howto_css_modals.asp
let modal = document.getElementById('new-board-modal');
// Button id. There is only one, so it is weird to use a classs... 
// but the id has the team id in jinja, so how can i get that in js?

// When the user clicks on the button, open the modal 
$("#new-board").on('click', function (evt) {
    //let teamId = $(this).data("teamId");
    modal.style.display = "block"; //changes css display value from none
});

// When the user clicks on <span> (x), close the modal
$('#modal-close').on('click', function (evt) {
    modal.style.display = "none"; //changes css display value from none
});

// javascript for an event listener
window.addEventListener("click", function (evt) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
});


/////////////////////////////////////////////////////////////////////////////
/// NEW PROJECT (ITEM OR IDEA) CODE ///
/////////////////////////////////////////////////////////////////////////////

// div with id all-board-projects starts with 'hidden' toggled on
$('.board-button').on('click', function (evt) {
    let boardId = $(this).data("boardId");

    // checks only the first div; if visible, toggles both off for the board
        // when the button is clicked (again)
    if ($("#show-projects-" + boardId).is(':visible')) {
        $(".show-projects").hide();  // Close the div with the projects
        $(".make-new-project").hide();  // Close the new project div
    // handles clicking another board, which is not yet visible (regardless if
        // any are visible)
    } else { 
        $(".show-projects").hide();
        $(".make-new-project").hide();
        $("#show-projects-" + boardId).show();
        $("#make-new-project-" + boardId).show();
    }
});

