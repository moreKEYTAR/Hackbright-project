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
/// EVENT LISTENER FOR SUBMITTING PROJECT DETAILS CHANGES ///
/////////////////////////////////////////////////////////////////////////////
// $('#project-details-form').on('submit', function (evt) {
    
// }); // closes submit event listener and function



/////////////////////////////////////////////////////////////////////////////
/// PROJECT DETAILS MODAL ///
/////////////////////////////////////////////////////////////////////////////

// When any project is double-clicked:
$('div.project').on('dblclick', function (evt) {
    let projectId = $(this).data("projectId");

    $.get("/view-details/"+projectId, function (results) {
        // results has the following keys:
            // userId, pOwnerId, pOwnerName, pTitle, pNotes, 
                // pPhase, pUpvotes, pUpdated

        // If the project is claimed...
        if (results.pOwnerId) {

            // ...by the current user who is logged in, display that info to 
                // the user, show notes field, and allow user to mark as done.


            if (results.pOwnerId === results.userId) {
                $('#project-details-project-owner'
                  ).html("You have claimed this item");
                $('#project-details-project-owner'
                  ).append('<br>');
                // Make checkbox so that user can "complete" the item
                let inputCheckbox = $('<input>');
                    inputCheckbox.attr({"type": "checkbox", 
                                        "name": "check-is-completed",
                                        "value": "done",
                                        "id": "check-item-as-done",
                                        "form": "project-details-form"});
                let checkLabel = $('<label>');
                    checkLabel.attr({"for": "check-item-as-done"});
                let checkSpan = $('<span>');
                    checkSpan.html("  Mark as Done");

                $('#project-details-project-owner').append(inputCheckbox);
                $('#project-details-project-owner').append(checkLabel);
                $('#project-details-project-owner').append(checkSpan);

                $("#project-details-notes-div").show();
            
            // ...by a different user, display that info, do not show option to
                // mark as done, do not show notes. Later: comments.

            } else {
                $('#project-details-project-owner'
                  ).html(results.pOwnerName+" is working on this item.");
                // Cannot edit notes, but can add comments. V2.0, pending
            }

        // If the item or idea is not claimed, show notes, allow save changes 
            // (form), show upvotes (PENDING), allow to upvote (PENDING), allow
            // user to claim it (PENDING)
        } else {
            $('#project-details-project-owner'
              ).html("Up for grabs!");
            $('#project-details-project-owner').append('<br>');
            // No owner of the project. Replicate the claim button, and allow
            // notes (V1.0); change notes to COMMENTS (V2.0, pending)
            $("#project-details-notes-div").show();  // hidden when modal closes
        }

        // Populate modal elements with information retrieved from db via route
        // Update empty h3 tag
        $('#project-details-title').html(results.pTitle);

        // Update empty action attribute in the form
        $('#project-details-notes-form').attr("action", 
                                               "/save-update/"+projectId);
        $('#project-details-notes-textarea').html(results.pNotes);

        // Everything is "loaded" before display is set to block (showing modal)
        $('#project-details-modal').css("display", "block");

    }); // closes function & ajax
}); // closes event listener function

// Close modal via the x span
$('#project-details-modal-close').on('click', function (evt) {
    $("#project-details-notes-div").hide(); 
        // Makes sure it hides so it will only show if the logic is met, when triggered
    $('#project-details-modal').css("display", "none"); 
        //changes css display value from none
});

// Close modal via clicking outside the modal content, into the modal background
let projectDetailsModal = document.getElementById('project-details-modal');
window.addEventListener("click", function (evt) {
    if (event.target == projectDetailsModal) {
        $("#project-details-notes-div").hide();
        // Makes sure it hides so it will only show if the logic is met, when triggered
        projectDetailsModal.style.display = "none";

    }
});



/////////////////////////////////////////////////////////////////////////////
/// NEW BOARD MODAL ///
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
/// NEW PROJECT MODAL ///
/////////////////////////////////////////////////////////////////////////////

// https://www.w3schools.com/howto/howto_css_modals.asp
let newProjectModal = document.getElementById('new-project-modal');

// When the user clicks on the button, open the modal 
$(".add-project-to-board-button").on('click', function (evt) {
    let boardId = $(this).data("boardId");
    let hiddenInput = document.querySelector('#new-project-hidden-input');
    hiddenInput.setAttribute('value', boardId);
      // this value will be reset with every click, so no need to "dump" boardId
    newProjectModal.style.display = "block";
      //changes css display value from none
});

// When the user clicks on <span> (x), close the modal
$('#project-modal-close').on('click', function (evt) {
    newProjectModal.style.display = "none"; //changes css display value from none
});

// javascript for an event listener
window.addEventListener("click", function (evt) {
    if (event.target == newProjectModal) {
        newProjectModal.style.display = "none";
    }
});



