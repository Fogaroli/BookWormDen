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
const $userPageLink = $('#user-page-link')


//================================================================
//Feature Functions

//function to create book markup
function addMarkup(book){
    /**Add html markup to the book entry before adding to the results page */
    const bookEntry = `
                <div class="row" id="${book.id}">
                    <div class="col-2 img-fluid">
                        <img
                            src="${book.thumbnail}"
                        />
                    </div>
                    <div class="col-10">
                        <div class="row">
                            <div class="col-12 h4">
                                ${book.title}
                            </div>
                            <div class="col-4">${book.authors}</div>
                            <div class="col-5"></div>
                            <div class="col-3 text-align-right">${book.publishedDate}</div>
                            <div class="col-12">
                                <small>
                                ${book.description}
                                </small>
                            </div>
                        </div>
                    </div>
                </div>

    `
    return $("<li>", {class:"list-group-item"}).html(bookEntry)
}
    

//function to convert search string to searcheable format.
function convertSearchString(inputString){
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
    return searchString
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


//procedure to update the overlay with book results
async function updateBookSearch(searchInput){
    const searchString = convertSearchString(searchInput)
    const bookList = await Book.getBookByTitle(searchString)
    if (!bookList){
        $bookSearchResults.append($("<p>", {text:"Error to connect to the search server, please try again."}))
    }else{

        bookList.forEach((bookVolume)=> {
            const bookEntry = addMarkup(bookVolume);
            $bookSearchResults.append(bookEntry)
        });
    }
    $bookListLoading.hide();
}


//================================================================
