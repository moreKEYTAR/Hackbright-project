"use strict";

$('#make-team').on('click', function (evt) {
    let newTeamName = $("#new-team-name").val();
    let newTeamDesc = $("#new-team-desc").val();
    $.post("/new-team", {"name": newTeamName, "desc": newTeamDesc}, function (results) {
        //assume results = {teamId: xxxxxx}
        let div = $("<div>");
        let form = $("<form>");  // makes a form element, still unattached
        form.attr({"action": "/view-team", "method": "GET"});
        div.append(form);   // makes form a child of the div...appending to the end of the child list
        
    });
}
);