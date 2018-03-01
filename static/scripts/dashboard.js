"use strict"; /*jslint node: true */




// div with id new-team starts with 'hidden' toggled on
$('#show-make-team').on('click', function (evt) {
    $('#new-team').toggleClass('hidden');
});

$('#trigger-make-team').on('click', function (evt) {
    let newTeamName = $("#new-team-name").val();
    let newTeamDesc = $("#new-team-desc").val();

    $.post("/new-team", {"name": newTeamName, "description": newTeamDesc}, 
        function (results) {
        // results = {teamId: xxxxxx}
            // Should I put these into a separate function?
            let div = $("<div>");
            let form = $("<form>");  // makes a form element, still unattached
                form.attr({"action": "/view-team", "method": "POST"});
            let inputHidden = $("<input>");
                inputHidden.attr({"type": "hidden", "name": "team", 
                                  "value": results.teamId});
            let inputSubmit = $("<input>");
                inputSubmit.attr({"type": "submit", "value": newTeamName});
            let descPara = $("<p>");
                descPara.attr({"class": "desc"});
                descPara.html(newTeamDesc);

            // Connecting our elements to each other and dashboard.html tree
            form.append(inputHidden);
            form.append(inputSubmit);
            form.append(descPara);
            div.append(form);
            $('#joined-teams').append(div);

            $("#new-team-name").val('');
            $("#new-team-desc").val('');
            
        }); // closes function & ajax

    $('#new-team').toggleClass('hidden');

    }); // close function & event listener
