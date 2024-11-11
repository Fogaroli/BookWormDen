/*
Title: The BookWormDen
Author: Fabricio Ribeiro
Date: October 6th, 2024
Description: This file handles the search functions and display of search results.
*/

//Global variables

const $searchButton = $("#book-search-button");
const $searchOverlay = $("#book-search-section");
const $bookSearchLoading = $("#book-list-loading-msg");
const $bookSearchResults = $("#book-search-results");
const $bookSearchForm = $("#book-search-form");
const $bookSearchInput = $("#book-search-input");
const $detailsOverlay = $("#book-details-section");
const $bookDetailsLoading = $("#book-details-loading-msg");
const $bookDetails = $("#book-details");
const userIsLogged = $("#user-page-link").length ? true : false;

//================================================================
//Supporting Functions

//function to create book search result markup
function addMarkup(book) {
    /**Add html markup to the book entry before adding to the results page */
    const bookEntry = `
                <div class="row">
                    <div class="col-2 img-fluid">
                        <img class="book-cover-image" id="${book.id}"
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

    `;
    return $("<li>", { class: "list-group-item" }).html(bookEntry);
}

//function to create book rating with star icons
function starRating(rating) {
    const starContainer = $("<span>");
    //TODO Improve this function to round to 0.5 star and use "fas fa-star-half-stroke"
    for (let i = 1; i <= 5; i++) {
        const star = $("<i>");

        if (i <= rating) {
            star.addClass("fas fa-star");
        } else {
            star.addClass("far fa-star");
        }
        starContainer.append(star);
    }
    return starContainer.prop("outerHTML");
}

//function to create book details markup
function addBookDetailsMarkup(book) {
    /**Add html markup to the book entry before adding to the results page */
    const bookEntry = `
                <div class="row">
                    <div class="col-2 img-fluid">
                        <div class="row">    
                            <img src="${book.thumbnail}"/>
                        </div>
                        <div class="row">
                            ${
                                userIsLogged
                                    ? `<form action="/user/add-book" method="POST">
                                <input name="api_id" value="${book.id}" hidden />
                                <input name="title" value="${book.title}" hidden />
                                <input name="cover" value="${book.thumbnail}" hidden />
                                <input name="authors" value="${book.authors}" hidden />
                                <input name="categories" value="${book.categories}" hidden />
                                <input name="description" value="${book.description}" hidden />
                                <input name="page_count" value="${book.page_count}" hidden />
                                <button type="submit" class="btn btn-light m-2" >Add to my reading list</button>
                                </form>`
                                    : ""
                            }
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
                            <div class="col-6 text-align-right">Published by ${
                                book.publisher
                            } in ${book.publishedDate}</div>
                        </div>
                        <div class="row">
                            <div class="col-4">${book.page_count} pages</div>
                            <div class="col-2"></div>
                            <div class="col-6 text-align-right">Rating ${starRating(
                                book.average_rating
                            )}</div>
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
                                <strong> Categories : </strong> ${
                                    book.categories
                                }
                                </small>
                            </div>
                        </div>
                    </div>
                </div>

    `;
    return $("<li>", { class: "list-group-item" }).html(bookEntry);
}

//function to convert search string to searchable format.
function convertSearchString(inputString) {
    let searchString = "";
    let inQuotes = false;

    for (let i = 0; i < inputString.length; i++) {
        if (inputString[i] === '"') {
            inQuotes = !inQuotes;
            searchString += '"';
        } else if (inputString[i] === " " && !inQuotes) {
            searchString += "+";
        } else {
            searchString += inputString[i];
        }
    }
    return searchString;
}

//================================================================
//DOM Manipulation

//----------------------------------------------------------------
//Event Listeners

//event listener to open the book search overlay
$searchButton.on("click", () => {
    $bookDetails.empty();
    $detailsOverlay.hide();
    $searchOverlay.show();
});

//event listener to close the book search overlay
$(document).on("click", (event) => {
    if (
        $searchOverlay.css("display") !== "none" &&
        event.target.closest("section") !== $searchOverlay[0] &&
        event.target.id !== `book-search-button`
    ) {
        $searchOverlay.hide();
    }
    if (
        $detailsOverlay.css("display") !== "none" &&
        event.target.closest("section") !== $detailsOverlay[0] &&
        !$(event.target).hasClass(`book-link`) &&
        !$(event.target).hasClass(`book-cover-image`)
    ) {
        $detailsOverlay.hide();
    }
});

//event listener for the book search button
$bookSearchForm.on("submit", (event) => {
    event.preventDefault();
    $bookSearchResults.empty();
    $bookSearchLoading.show();
    updateBookSearch($bookSearchInput.val());
});

//create event listeners for book search results
function setBookListeners() {
    $(`.book-link`).on("click", showBookDetails);
    $(`.book-cover-image`).on("click", showBookDetails);
}

//----------------------------------------------------------------
// DOM manipulation procedures

//procedure to update the overlay with book results
async function updateBookSearch(searchInput) {
    const searchString = convertSearchString(searchInput);
    const bookList = await Book.getBookByTitle(searchString);
    if (!bookList) {
        $bookSearchResults.append(
            $("<p>", {
                text: "Error to connect to the search server, please try again.",
            })
        );
    } else {
        bookList.forEach((bookVolume) => {
            const bookEntry = addMarkup(bookVolume);
            $bookSearchResults.append(bookEntry);
        });
        setBookListeners();
    }
    $bookSearchLoading.hide();
}

//procedure to clear search results and show specific book details content
async function showBookDetails(event) {
    $searchOverlay.hide();
    $bookDetails.empty();
    $detailsOverlay.show();
    $bookDetailsLoading.show();
    const bookId = event.target.id;
    const bookData = await Book.getBookDetailById(bookId);
    if (!bookData) {
        $bookDetails.append(
            $("<p>", {
                text: "Error get book details from server, please try again.",
            })
        );
    } else {
        const bookEntry = addBookDetailsMarkup(bookData);
        $bookDetails.append(bookEntry);
    }
    $bookDetailsLoading.hide();
}

//================================================================
//Setup for unit testing

if (typeof module !== "undefined" && module.exports) {
    module.exports = {
        addMarkup,
        starRating,
        addBookDetailsMarkup,
        convertSearchString,
        updateBookSearch,
        showBookDetails,
    };
}
