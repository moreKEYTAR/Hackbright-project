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
    let allParents = ($(this).parents());
    
    let grandparent = allParents[1];
    // Need to set the new class on the grandparent, regardless whether it was
        // an item or idea, so that the display is for an item
    console.log(grandparent);

    $.post ("/claim-project", {"projectId": projectId}, function (results) {
            // results is a dictionary, with the board id?
        
        // Select, out of the class of accept-project-buttons, the one
        // where the data attribute is exactly data-project-id=projectId
        let claimButton = $(
            '.accept-project-button[data-project-id='+projectId+']');
        claimButton.hide();
            // Claim button is now hidden until page refresh, 
            // when it will not be generated

        grandparent.className ='project-content-item';

        // Print the string that was returned
        console.log(results);
        // Fade message to confirm success to user, from website:
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

    // Modal content is based on showing / hiding the correct div (currently)
    $(".project-details-div").hide();

    $.get("/view-details/"+projectId, function (results) {
        // results has the following keys:
            // userId, pOwnerId, pOwnerName, pTitle, pNotes, 
                // pPhase, pUpvotes, pUpdated

        // Populate general info
        // Title in h3 div:
        $('#project-details-title').html(results.pTitle);

        // If the project is an idea (and therefore not claimed)?
        if (results.pPhase === "idea") {
            
            // no ownership if an idea ????
            // there is a form in this div, with no action
            // Update notes textarea...no current way to update
            $('#pd-idea-textarea').html(results.pNotes);

            // Show the correct div
            $('#pd-idea-div').show();
        }
        
        // If the project is an item (which is the only other kind of 
            // clickable on this page)...
        else if (results.pPhase === "item") {

            // There is no owner...
            if (!results.pOwnerId) {
                $("#project-details-unclaimed-div").show();
            
            
            // If the project is claimed, and it is by the current user...
            } else if (results.pOwnerId, 
                     results.pOwnerId === results.userId) {

                // Update the form submission action
                $('#project-details-owner-form'
                  ).attr({"action": "/save-update/"+projectId});

                // Update the notes content
                $('#pd-notes-textarea-is-owner').html(results.pNotes);

                // Show the correct div
                $('#project-details-owner-div').show();
            
            // The owner is NOT the current user...
            } else if (results.pOwnerId, 
                       results.pOwnerId !== results.userId){
                $('#owner-info-not-user'
                  ).html(results.pOwnerName+" is working on this item.");

                // Show the correct div
                $('#project-details-not-owner-div').show();

            } // Close else if for results.pOwnderId

        } // Close else if for item

        // Everything is "loaded" before display is set to block (showing modal)
        $('#project-details-modal').css("display", "block");

    }); // closes function & ajax
}); // closes event listener function

// Close modal via the x span
$('#project-details-modal-close').on('click', function (evt) {
        // Makes sure it hides so it will only show if the logic is met, when triggered
    $('#project-details-modal').css("display", "none"); 
        //changes css display value from none
});

// Close modal via clicking outside the modal content, into the modal background
let projectDetailsModal = document.getElementById('project-details-modal');
window.addEventListener("click", function (evt) {
    if (event.target == projectDetailsModal) {
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



