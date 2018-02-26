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
            // results is a dictionary, with the board id?
        
        // Select, out of the class of accept-project-buttons, the one
        // where the data attribute is exactly data-project-id=projectId
        let claimButton = $(
            '.accept-project-button[data-project-id='+projectId+']');
        claimButton.hide();
        console.log(results);
        
        // fade message to confirm success to user, from website:
            // http://jsfiddle.net/sunnypmody/XDaEk/
        $( "#success-claimed-project" ).fadeIn( 300 ).delay( 1500 ).
        fadeOut( 400 );
        }); // closes function & ajax
    }); // closes event listener function


/////////////////////////////////////////////////////////////////////////////
/// PROJECT DETAILS MODAL ///
/////////////////////////////////////////////////////////////////////////////

// When any project is double-clicked:
$('div.project').on('dblclick', function (evt) {
    let projectId = $(this).data("projectId");

    $.get("/view-details/"+projectId, function (results) {
            // results is a dictionary with all project details

        // Update empty h3 tag
        $('#project-details-title').html(results.p_title);

        // Update empty action attribute in the form
        $('#update-project-details-form').attr("action", 
                                               "/save-update/"+projectId);
        $('#project-details-textarea').html(results.p_notes);
        $('#project-details-modal').css("display", "block");

    }); // closes function & ajax
}); // closes event listener function


$('#project-details-modal-close').on('click', function (evt) {
    $('#project-details-modal').css("display", "none"); 
        //changes css display value from none
});

let projectDetailsModal = document.getElementById('project-details-modal');
window.addEventListener("click", function (evt) {
        if (event.target == projectDetailsModal) {
        projectDetailsModal.style.display = "none";
    }
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



