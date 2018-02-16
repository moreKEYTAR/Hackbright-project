"use strict";


function makeTeamElements() {




$('#make-team').on('click', function (evt) {
    let newTeamName = $("#new-team-name").val();
    let newTeamDesc = $("#new-team-desc").val();
    $.post("/new-team", {"name": newTeamName, "desc": newTeamDesc}, 
        function (results) {
        // results = {teamId: xxxxxx}
            // Should I put these into a separate function?
        let div = $("<div>");
        let form = $("<form>");  // makes a form element, still unattached
            form.attr({"action": "/view-team", "method": "GET"});
        let inputTeamId = $("<input>");
            inputTeamId.attr({"type": "hidden", "name": "team", 
                              "value": results.teamId});
        let inputSubmit = $("<input>");
            inputSubmit.attr({"type": "submit", "value": newTeamName});
        let descPara = $("<p>");
            descPara.attr({"class": "desc"});
            desc.Para.html(newTeamDesc);

        // Connecting our elements to each other and dashboard.html tree
        form.append(inputTeamId);
        form.append(inputSubmit);
        form.append(descPara);
        div.append(form);
        $('#joined-teams').append(div);
        });
    });
}
);