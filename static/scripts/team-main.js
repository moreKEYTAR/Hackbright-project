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
/// CLAIM PROJECT CODE ///
/////////////////////////////////////////////////////////////////////////////

$('.accept-project-button').on('click', function (evt) {
    let projectId = $(this).data("projectId");
    $.post ("/claim-project", {"projectId": projectId}, function (results) {
        alert("Claimed!");
    }); // closes function & ajax

});


/////////////////////////////////////////////////////////////////////////////
/// MODAL CODE: NEW BOARD MODAL ///
/////////////////////////////////////////////////////////////////////////////

// https://www.w3schools.com/howto/howto_css_modals.asp
let boardModal = document.getElementById('new-board-modal');

// When the user clicks on the button, open the modal 
$("#new-board-button").on('click', function (evt) {
    boardModal.style.display = "block"; //changes css display value from none
});

// When the user clicks on <span> (x), close the modal
$('#board-modal-close').on('click', function (evt) {
    boardModal.style.display = "none"; //changes css display value from none
});

// javascript for an event listener
window.addEventListener("click", function (evt) {
    if (event.target == boardModal) {
        boardModal.style.display = "none";
    }
});


/////////////////////////////////////////////////////////////////////////////
/// MODAL CODE: NEW PROJECT MODAL ///
/////////////////////////////////////////////////////////////////////////////

// https://www.w3schools.com/howto/howto_css_modals.asp
let projectModal = document.getElementById('new-project-modal');

// When the user clicks on the button, open the modal 
$(".add-project-to-board-button").on('click', function (evt) {
    let boardId = $(this).data("boardId");
    projectModal.style.display = "block"; //changes css display value from none
});

// When the user clicks on <span> (x), close the modal
$('#project-modal-close').on('click', function (evt) {
    projectModal.style.display = "none"; //changes css display value from none
});

// javascript for an event listener
window.addEventListener("click", function (evt) {
    if (event.target == projectModal) {
        projectModal.style.display = "none";
    }
});



