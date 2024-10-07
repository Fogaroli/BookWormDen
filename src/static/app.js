/*
Title: The BookWormDen
Author: Fabricio Ribeiro
Date: October 6th, 2024
*/

//Global variables

const $searchButton = $("#book-search-button")
const $searchOverlay = $("#book-search-section")
const $bookListLoading = $("#book-list-loading-msg")
const $bookSearchResults = $("#book-search-results")
const $bookSearchForm = $("#book-search-form")
const $bookSearchInput = $('#book-search-input')


//================================================================
//Feature Functions

//function to create book markup

//async function to read data from the backend
async function getBookList(seachString){

};



//function to fill book results
async function performBookSearch(inputString){
    let searchString = '';
    let inQuotes = false;
    
    for (let i = 0; i < inputString.length; i++) {
        if (inputString[i] === '"') {
            inQuotes = !inQuotes;
            searchString += '"';
        } else if (inputString[i] === ' ' && !inQuotes) {
            searchString += '+';
        } else {
            searchString += inputString[i];
        }
    }
    console.log(searchString)
    try {
        response = await getBookList(searchString)
    } catch{
        
    }
}

//================================================================
//DOM Manipulation Functions

//event listener to open the book search overlay
$searchButton.on("click", () => {
    $searchOverlay.show()
});

//event listener to close the book seach overlay
$(document).on("click", (event) =>{
    if ($searchOverlay.css('display') !== 'none' && !$searchOverlay[0].contains(event.target) && !$searchButton[0].contains(event.target)){
        $searchOverlay.hide()
    }
})

//event listener for the book search button
$bookSearchForm.on("submit", (event) =>{
    event.preventDefault()
    $bookSearchResults.empty()
    $bookListLoading.show()
    updateBookSearch($bookSearchInput.val())
})


//function to update the overlay with book results
async function updateBookSearch(searchInput){
    bookList = await performBookSearch(searchInput)
}


//================================================================
