"use strict"; /*jslint node: true */

// default value of log-in set in route
let userChoice = $('#hidden-u-choice').data("choice");

if (userChoice == "sign-up") {
    console.log("one");
    $('#log-in-form').hide();
    $('#register-new-user-form').show();
} else {
    console.log("two");
    $('#register-new-user-form').hide();
    $('#log-in-form').show();
}

// // https://www.sitepoint.com/full-screen-bootstrap-carousel-random-initial-image/
// // Get all carousel items (img div wrappers)
// let $item = $('.carousel-item');
// // Get jQuery object representing size...never seen it this way before
// let $wdwHeight = $(window).height();
// // Set height of all images to window height
// $item.height($wdwHeight);
// // Add full-screen class to all items (.fullscreen styled in css..
//         // could have manually added, but we were already grabbing all elements)
// $item.addClass('full-screen'); // full-screen bootstrap class

// // Loop through each IMAGE:
//     // select img elements descending from the carousel
// $('.carousel img').each(function () {
//     // getting value of src (the file address) and its color attr (I have removed)
//     let $src = $(this).attr('src');
//     // let $color = $(this).attr('data-color');

//     // find the parent, which is carousel-item and is class full-screen, 
//         // and set its background as the img (img fills the whole div, 
//             // which should be the whole page)
//     $(this).parent().css( {
//         'background-image': 'url('+$src+')',  //assign the image to the backround-image attribute
//         // 'background-color': $color
//         });
//     $(this).remove(); //removes the "double" image from existing inside itself
//     // (what a wild way to do this...need to study!)
// });

// // event listener in jQuery for resizing window
// $(window).on('resize', function () {
//     $wdwHeight = $(window).height(); // update window height to new size
//     $item.height($wdwHeight);  
//         // note it resizes the item div, to keep with the window's height not width
// });


// // https://www.w3schools.com/jquery/traversing_eq.asp
// //  again grabbing all item divs, indexed (cool!), apply this method to that nth thing:
// $item.eq(0).addClass('active');
//     // From website:
//         // This allows us to prevent a small toggle that is possible to occur 
//             // between the two different heights (before and after the changes 
//                 // we made) of the first slide.

$('.carousel').carousel({
  interval: 4800,
  pause: "false"
});
