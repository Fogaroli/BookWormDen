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
const userIsLogged = $('#user-page-link').length ? true : false


//================================================================
//Feature Functions

//function to create book search result markup
function addMarkup(book){
    /**Add html markup to the book entry before adding to the results page */
    const bookEntry = `
                <div class="row">
                    <div class="col-2 img-fluid">
                        <img
                            src="${book.thumbnail}"
                        />
                    </div>
                    <div class="col-10">
                        <div class="row">
                            <div class="col-12 h4">
                                <strong class="book-link" id="${book.id}">${book.title}</strong>
                            </div>
                        </div>
                        <div class="row">
                            <div class="col-4">${book.authors}</div>
                            <div class="col-5"></div>
                            <div class="col-3 text-align-right">${book.publishedDate}</div>
                        </div>

                        <div class="row">
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

//function to create book rating with start icons
function starRating(rating){
    const starContainer = $("<span>");
    //TODO Improve this function to round to 0.5 start and use "fas fa-star-half-stroke"
    for (let i = 1; i <= 5; i++) {
      const star = $("<i>");
     
      if (i <= rating) {
        star.addClass('fas fa-star');
      } else {
        star.addClass('far fa-star');
      }
      starContainer.append(star);
    }
    return starContainer.prop('outerHTML')
}


//function to create book details markup
function addBookDetailsMarkup(book){
    /**Add html markup to the book entry before adding to the results page */
    const bookEntry = `
                <div class="row">
                    <div class="col-2 img-fluid">
                        <div class="row">    
                            <img src="${book.thumbnail}"/>
                        </div>
                        <div class="row">
                            ${userIsLogged ? 
                                `<form action="/book/${book.id}/add-to-user" method="POST">
                                <input name="book_title" value="${book.title}" hidden />
                                <button type="submit" class="btn btn-light m-2" >Add to my reading list</button>
                                </form>`
                                : "" }
                        </div>
                    </div>
                    <div class="col-10">
                        <div class="row">
                            <div class="col-12 h4">
                                <strong>${book.title}</strong>
                            </div>
                        </div>
                        <div class="row">
                            <div class="col-4">${book.authors}</div>
                            <div class="col-2"></div>
                            <div class="col-6 text-align-right">Published by ${book.publisher} in ${book.publishedDate}</div>
                        </div>
                        <div class="row">
                            <div class="col-4">${book.page_count} pages</div>
                            <div class="col-2"></div>
                            <div class="col-6 text-align-right">Rating ${starRating(book.average_rating)}</div>
                        </div>
                        <div class="row mt-3">
                            <div class="col-12">
                                <small>
                                ${book.description}
                                </small>
                            </div>
                        </div>
                        <div class="row">
                            <div class="col-12">
                                <small>
                                <strong> Categories : </strong> ${book.categories}
                                </small>
                            </div>
                        </div>
                    </div>
                </div>

    `
    return $("<li>", {class:"list-group-item"}).html(bookEntry)
}

//function to convert search string to searchable format.
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

//event listener to close the book search overlay
$(document).on("click", (event) =>{
    if ($searchOverlay.css('display') !== 'none' && event.target.closest("section") !== $searchOverlay[0] && !$searchButton[0].contains(event.target)){
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
        $(`.book-link`).on('click', showBookDetails)
    }
    $bookListLoading.hide();
}

//procedure to clear search results and show specific book details content
async function showBookDetails(event){
    console.log($searchOverlay.css('display') !== 'none', event.target.closest("section") !== $searchOverlay[0], !$searchButton[0].contains(event.target))
    $bookListLoading.show()
    const bookId = event.target.id
    const bookDetails = await Book.getBookDetailById(bookId)
    if (!bookDetails){
        $bookSearchResults.append($("<p>", {text:"Error get book details from server, please try again."}))
    }else{
        $bookSearchResults.empty()
        const bookEntry = addBookDetailsMarkup(bookDetails);
        $bookSearchResults.append(bookEntry)
    }
    $bookListLoading.hide();
}