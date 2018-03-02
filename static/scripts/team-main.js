"use strict"; /*jslint node: true */


/////////////////////////////////////////////////////////////////////////////
/// DRAG AND DROP FOR PROJECTS ///
/////////////////////////////////////////////////////////////////////////////
/* To dos for drag and drop:
    - make projects draggable DONE
    - make the dock droppable
    - make areas force a drag snap back (undroppable)
    - make the dock auto-populate with divs with all projects that the logged in 
        user owns for that team...regardless of board
    - make the display of the items that the user owns, when seen in the board, 
        be more transparent or something
    - make the drop onto the dock have meaning and effects, including:
        - updating ownership IF the project is up for grabs
            (and therefore, the claim button is no longer needed on the 
                project itself)
        - doing nothing else if the project is NOT up for grabs
        - making the project now live in the dock too, larger 
        - completing the project removes it from the dock...and completing 
            it can ALSO be done by dragging
        - can also drag to backlog, which changes the status
    ---> need the interactive board area to be able to go wide and be fixed
    --> need help with logic for this
*/

function updateInteractivity () {
    $('.project').draggable( {
        cursor: "move",
        //revert: true, I ONLY WANT REVERT TO HAPPEN IF IT GOES INTO A FORBIDDEN ZONE
        // helper: "clone",
        // stack: ".project",
        drag: function( event, ui ) {
            $(this).css("opacity", "0.8");
        },
        stop: function( event, ui ) {
            $(this).css("opacity", "1.0");
        }
    });


    $('.project-in-dock').draggable( {
        cursor: "move",
        drag: function( event, ui ) {
            $(this).css("opacity", "0.8");
        },
        stop: function( event, ui ) {
            $(this).css("opacity", "1.0");
        }
    });

    $('.dock').droppable( {
        drop: function( event, ui ) {
            let projectIdDragged = ui.draggable.attr("data-project-id");
            let projectClassDragged = ui.draggable.attr("class");
            let pClassLst = projectClassDragged.split(" ");
            if (pClassLst[0] === "project") {

                console.log(ui);
                console.log(ui.parents());
                //console.log($(allParents[1]));










                // pending
















                aleiljfi;
                let payload = {"projectId": projectIdDragged};
                $.post("/claim-project", payload, function (results) {
                    console.log("end of post method request");
                    console.log(results);
                });
            } else {
                console.log("booooo");
            }




    // let projectId = $(this).data("projectId");
    // let allParents = ($(this).parents());
    // let grandparent = $(allParents[1]);
    // let grandClass = grandparent.attr("class");

    // let payload = {"projectId": projectId,
    //                "grandClass": grandClass};

            //let dockId = $(this).attr("id");
            // other class: project-in-dock
        }
        // over: function(evt, ui) {
        //     $('.dock').css("background-color", "#00b3b3");
        //}
    }); // closes $('.dock').droppable...
} // closes updateInteractivity...



// drop: function(event, ui) {     
//       let draggedID = ui.draggable.attr("id");
//       let droppableID = $(this).attr("id");

// $(this).css("background-color", "lightgreen")}              

//       let payload = {"colorPick": draggedID};
      
// $.post("/record-color", payload, function 
//             (results) {     
//         alert(`Vote recorded for ${results}!`);
//       });
//     }






updateInteractivity();


/////////////////////////////////////////////////////////////////////////////
/// FUNCTION TO HAVE MOST RECENT BOARD OPEN ///
/////////////////////////////////////////////////////////////////////////////

function showRecentBoard() {
    let currentBoard = $('#current-board-info').attr("value");
    if (currentBoard === "None") {
        console.log("Boards all closed.");
    } else {
        $(".show-projects").hide();
        $(".make-new-project").hide();
        $("#show-projects-" + currentBoard).show();
        $("#make-new-project-" + currentBoard).show();
}}
showRecentBoard();


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
        $('#current-board-info').attr({"value": "None"});

    // handles clicking another board, which is not yet visible (regardless if
        // any are visible)
    } else {
        $(".show-projects").hide();
        $(".make-new-project").hide();
        $("#show-projects-" + boardId).show();
        $("#make-new-project-" + boardId).show();

    }

    // Route updates session with most recent board.
    $.post("/current-board", {"boardId": boardId}, function (results) {
        console.log(results);
        $('#current-board-info').attr({"value": boardId});

    });
        
});


/////////////////////////////////////////////////////////////////////////////
/// CLAIM PROJECT BUTTON ///
/////////////////////////////////////////////////////////////////////////////


function updateProjectOwnership(results) {
    // Results keys: 
        // "displayname", "projectTitle", "projectNotes", "projectId", "grandClass"

    let pId = results.projectId;

    // Select, out of the class of accept-project-buttons, the one
    // where the data attribute is exactly data-project-id=projectId
    let claimButton = $(
        '.accept-project-button[data-project-id='+pId+']');
    claimButton.hide();

    // Make sure that the class is updated for the project-content... div
    let projectContentDiv = $('.project[data-project-id='+pId+']').children('div')[0];
    projectContentDiv.className = 'project-content-item';

    let upvotesDiv = $('.upvotes[data-project-id='+pId+']');
    if (upvotesDiv) {
        upvotesDiv.hide();
    }

    // update the user's name to the claimed project in the board area
    let appendDiv = $('.project-content-item[data-project-id='+pId+']');
    let nameHeading = $('<h5>');
        nameHeading.html(results.displayname);
    appendDiv.append(nameHeading);

    // update the dock with the project
    let dockDiv = $('<div>');
        dockDiv.attr({"class": "project-in-dock",
                      "data-project-id": ''+pId+''});
    let dockDivContent = $('<div>');
        dockDivContent.attr({"class": "project-content-in-dock",
                             "data-project-id": ''+pId+''});
    let projectHeading = $('<h5>');
        projectHeading.html(results.projectTitle);
    let hiddenNotesInput = $('<input>');
        hiddenNotesInput.attr({"type": "hidden",
                          "name": "notes",
                          "value": ''+results.projectNotes+''});
    let nameHeadingTwo = $('<h5>');
        nameHeadingTwo.html(results.displayname);

    dockDiv.append(dockDivContent);
    dockDivContent.append(projectHeading);
    dockDivContent.append(hiddenNotesInput);
    dockDivContent.append(nameHeadingTwo);
    $('#dock-projects-all').append(dockDiv);

    // update the draggable & droppable properties for these items, as needed
    updateInteractivity();

    // Fade message to confirm success to user, from website:
        // http://jsfiddle.net/sunnypmody/XDaEk/
    $( "#success-claimed-project" ).fadeIn( 300 ).delay( 2000 ).
    fadeOut( 400 );
}

$('.accept-project-button').on('click', function (evt) {
    let projectId = $(this).data("projectId");
    let allParents = ($(this).parents());
    let grandparent = $(allParents[1]);
    let grandClass = grandparent.attr("class");
    // grandClass needed to identify the correct div in the callback fn
        //Will need to set the new class on the grandparent for correct css
    let payload = {"projectId": projectId,
                   "grandClass": grandClass};

    $.post ("/claim-project", payload, updateProjectOwnership); 
    // // Results keys: "displayname", "statusMessage", "projectTitle", "projectNotes"

    //     // Print the string that was returned
    //     console.log(results.statusMessage);
    //     // Select, out of the class of accept-project-buttons, the one
    //     // where the data attribute is exactly data-project-id=projectId
    //     let claimButton = $(
    //         '.accept-project-button[data-project-id='+projectId+']');
    //     claimButton.hide();
    //         // Claim button is now hidden until page refresh, 
    //         // when it will not be generated

    //     grandparent.className ='project-content-item';
    //     let upvotesDiv = $('.upvotes[data-project-id='+projectId+']');
    //     if (upvotesDiv) {
    //         upvotesDiv.hide();
    //     }
 
    //     // update the user's name to the claimed project in the board area
    //     let appendDiv = $('.project-content-item[data-project-id='+projectId+']');
    //     let nameHeading = $('<h5>');
    //         nameHeading.html(results.displayname);
    //     appendDiv.append(nameHeading);

    //     // update the dock with the project
    //     let dockDiv = $('<div>');
    //         dockDiv.attr({"class": "project-in-dock",
    //                       "data-project-id": ''+projectId+''});
    //     let dockDivContent = $('<div>');
    //         dockDivContent.attr({"class": "project-content-in-dock",
    //                              "data-project-id": ''+projectId+''});
    //     let projectHeading = $('<h5>');
    //         projectHeading.html(results.projectTitle);
    //     let hiddenNotesInput = $('<input>');
    //         hiddenNotesInput.attr({"type": "hidden",
    //                           "name": "notes",
    //                           "value": ''+results.projectNotes+''});
    //     let nameHeadingTwo = $('<h5>');
    //         nameHeadingTwo.html(results.displayname);

    //     dockDiv.append(dockDivContent);
    //     dockDivContent.append(projectHeading);
    //     dockDivContent.append(hiddenNotesInput);
    //     dockDivContent.append(nameHeadingTwo);
    //     $('#dock-projects-all').append(dockDiv);

    //     updateInteractivity();
    //     // Fade message to confirm success to user, from website:
    //         // http://jsfiddle.net/sunnypmody/XDaEk/
    //     $( "#success-claimed-project" ).fadeIn( 300 ).delay( 2000 ).
    //     fadeOut( 400 );
    // }); // closes function & ajax

}); // closes event listener function



/////////////////////////////////////////////////////////////////////////////
/// INVITE TEAMMATES MODAL ///
/////////////////////////////////////////////////////////////////////////////

// CSS keeps modal hidden to start
let teammateInviteModal = document.getElementById('invite-teammates-modal');

// When the user clicks on the button, open the modal 
$('#invite-teammates-button').on('click', function (evt) {
    teammateInviteModal.style.display = "block";

});

// When the user clicks on <span> (x), close the modal
$('#invite-teammates-modal-close').on('click', function (evt) {
    teammateInviteModal.style.display = "none"; 
    $("#email-address-default").val('');
});

// javascript for an event listener
window.addEventListener('click', function (evt) {
    if (event.target == teammateInviteModal) {
        teammateInviteModal.style.display = "none";
        $("#email-address-default").val('');
    }
});

// Update modal with more rows in the team-invitations-form;
let addEntry = document.getElementById('add-email-invite-inputs-button');
$(addEntry).on('click', function (evt) {
    // make a new entry row for an email invitation
    let div = $("<div>");
        div.attr({"class": "add-email-invite-div"});
    let plusSpan = $("<span>");
        plusSpan.html("&#43;");
    let wordsSpan = $("<span>");
        wordsSpan.html(" Teammate's email address:");
    let newInput = $("<input>");
        newInput.attr({"type": "text", 
                       "maxlength": "254", 
                       "style": "width:200px", 
                       "name": "email",
                       "placeholder": "email address",
                       "form": "team-invitations-form"});
        newInput.prop("required", true);
    let newTextarea = $("<textarea>");
    let emailText = $( "#textarea-template-team-invites" ).html();
        newTextarea.html(emailText);
        newTextarea.attr({"form": "team-invitations-form",
                          "name": "email-message",
                          "rows": "3",
                          "cols": "40"});

    $("#email-input-area").append(div);
    div.append(plusSpan);
    div.append(wordsSpan);
    div.append(newInput);
    div.append(newTextarea);
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

            // $('#pd-idea-textarea').html(results.pNotes);

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


