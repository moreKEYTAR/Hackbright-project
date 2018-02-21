"use strict"; /*jslint node: true */

// div with id all-board-projects starts with 'hidden' toggled on
$('.board-button').on('click', function (evt) {
    let boardId = $(this).data("boardId");
    // the .data jquery method turns your data attribute kebab case into camel case by itself it is a witch
    // the .data() contains the rest of the data-stuff string, not what it is set equal to
        //.val is only for an input element. learning.
        //all data attributes come as a string because html sends strings
    $(".show-projects").hide();
    $(".make-new-project").hide();
    $("#show-projects-" + boardId).show();
    $("#make-new-project-" + boardId).show();
});




// $('#show-make-board').on('click', function (evt) {
//     $('#new-board').toggleClass('hidden');
// });


// <div class="board" id="{{ board.b_id }}">
//         <button type="button" class="board-button">{{ board.name }}</button>
//         <p class="description">{{ board.desc }}</p>
        
//         {% if board.projects %}
          
//           <div id="all-board-projects" class="hidden">
            
//             {% for project in board.projects %}
//               <br>
//               <div class="project" 
//                    id="{{ project.p_id }}" 
//                    data-parent="{{board.b_id}}" 
//                    data-phase="{{ project.phase_code }}"
//                    data-claiming-user="{{ project.user_id }}"
//                    data-updated="{{ project.updated }}">