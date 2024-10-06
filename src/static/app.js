/*
Title: The BookWormDen
Author: Fabricio Ribeiro
Date: October 6th, 2024
*/

//Global variables

const $searchButton = $("#book-search-button")
const $searchOverlay = $("#book-search-section")
const $bookListLoading = $("#book-list-loading-msg")


//================================================================
//Feature Functions



//================================================================
//DOM Manipulation Functions

$searchButton.on("click", () => {
    $searchOverlay.show()
});

$(document).on("click", (event) =>{
    if ($searchOverlay.css('display') !== 'none' && !$searchOverlay[0].contains(event.target) && !$searchButton[0].contains(event.target)){
        $searchOverlay.hide()
    }
})


//================================================================
