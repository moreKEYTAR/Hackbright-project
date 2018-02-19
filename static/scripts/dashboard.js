"use strict";

// div with id new-team starts with 'hidden' toggled on
$('#show-make-team').on('click', function (evt) {
    $('#new-team').toggleClass('hidden');
});

$('#make-team').on('click', function (evt) {
    let newTeamName = $("#new-team-name").val();
    let newTeamDesc = $("#new-team-desc").val();

    $.post("/new-team", {"name": newTeamName, "description": newTeamDesc}, 
        function (results) {
        // results = {teamId: xxxxxx}
            // Should I put these into a separate function?
            let div = $("<div>");
            let form = $("<form>");  // makes a form element, still unattached
                form.attr({"action": "/view-team", "method": "GET"});
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
            // $('#new-team').toggleClass('hidden');
            //
            //
            //SHOULD I WORRY ABOUT PLACEHOLDERS???



        }); // closes function & ajax

// reset form fields
//fifth attempt
    //$("#new-team-name").reset();
    //$("#new-team-desc").reset();
        //fourth attempt
        // $('input:text').focus(
        //     function() {
        //         $(this).val('');
        //     })
            // third attempt
            // $('#new-team').each(function () {
            //     $(this).val('');
            // }

                // second attempt
                // document.getElementById("new-team-name").reset();
                // document.getElementById("new-team-desc").reset();
                    // original attempt:
                    // $('input[type="text"]').val('');
                    // $('textarea').val('');
    }); // close function & event listener
