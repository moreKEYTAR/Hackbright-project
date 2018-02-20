"use strict";

// div with id new-team starts with 'hidden' toggled on
$('#show-make-board').on('click', function (evt) {
    $('#new-board').toggleClass('hidden');
});

$('#trigger-make-board').on('click', function (evt) {
    let newBoardName = $("#new-board-name").val();
    let newBoardDesc = $("#new-board-desc").val();
    let teamIdInfo = $("#team-id-info").val();

    $.post("/new-board", {"name": newBoardName, 
                          "description": newBoardDesc, 
                          "team-id-info": teamIdInfo},
            function (results) {
            // results need to give back Board's Id; we have team Id, name 
                //and description.... {boardId: integer}
            let div = $('<div>');
                div.attr({"class": "board"});
            let navLink = $('<a>');
                navLink.attr({"href": "/view-board"});
            let navButton = $('<button>');
                navButton.attr({"type": "button", "id": `${results.boardId}`});
                navButton.html(newBoardName);
            let boardDesc = $('h5');
                boardDesc.html(newBoardDesc);
            let inputHidden = $('input');
                inputHidden.attr({"type": "hidden", "name": "team", 
                                 "value": `${teamIdInfo}`});

            // Link elements from inner to outer
            navLink.append(navButton);  //navButton is a child of navLink

            // appending the div with each element in order
            div.append(navLink);  
            div.append(boardDesc);
            div.append(inputHidden);

            $('#all-team-boards').append(div);
            });
    $('#new-board').toggleClass('hidden');
});



