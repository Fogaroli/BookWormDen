/*
Title: The BookwormDen
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
    const template = document
        .getElementById("book-search-result-template")
        .content.cloneNode(true);

    template.querySelector(".book-cover-image").src = book.thumbnail;
    template.querySelector(".book-cover-image").id = book.id;
    template.querySelector(".book-link").textContent = book.title;
    template.querySelector(".book-link").id = book.id;
    template.querySelector(".book-authors").textContent = book.authors;
    template.querySelector(".book-published-date").textContent =
        book.publishedDate;
    template.querySelector(".book-description").textContent = book.description;

    return template;
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
    const template = document
        .getElementById("book-details-template")
        .content.cloneNode(true);

    template.querySelector(".book-thumbnail").src = book.thumbnail;
    template.querySelector(".book-title").textContent = book.title;
    template.querySelector(".book-authors").textContent = book.authors;
    template.querySelector(
        ".book-publisher"
    ).textContent = `Published by ${book.publisher} in ${book.publishedDate}`;
    template.querySelector(
        ".book-page-count"
    ).textContent = `${book.page_count} pages`;
    template.querySelector(".book-rating").innerHTML = starRating(
        book.average_rating
    );
    template.querySelector(".book-description").textContent = book.description;
    template.querySelector(".book-categories").textContent = book.categories;

    const form = template.querySelector(".add-book-form");
    form.querySelector('input[name="api_id"]').value = book.id;
    form.querySelector('input[name="title"]').value = book.title;
    form.querySelector('input[name="cover"]').value = book.thumbnail;
    form.querySelector('input[name="authors"]').value = book.authors;
    form.querySelector('input[name="categories"]').value = book.categories;
    form.querySelector('input[name="description"]').value = book.description;
    form.querySelector('input[name="page_count"]').value = book.page_count;

    if (!userIsLogged) {
        form.remove();
    }

    return template;
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
        setBookListeners,
    };
}
