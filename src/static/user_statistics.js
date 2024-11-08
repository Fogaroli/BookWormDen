/*
Title: The BookWormDen
Author: Fabricio Ribeiro
Date: October 6th, 2024
Description: This file handles user page and reading statistics for the books in the user reading list.
*/

//global variables

const bookDescription = document.querySelector("#book-description");
const bookStatistics = document.querySelector("#book-statistics");
const bookComments = document.querySelector("#book-comments");
const bookAddComment = document.querySelector("#book-addcomment");
const divDescription = document.querySelector("#div-description");
const divStatistics = document.querySelector("#div-statistics");
const divComments = document.querySelector("#div-comments");
const divAddComment = document.querySelector("#div-addcomment");

//================================================================
//Supporting Functions

//================================================================
//DOM Manipulation

//----------------------------------------------------------------
//Event Listeners

bookDescription.addEventListener("click", showDescription);
bookStatistics.addEventListener("click", showStatistics);
bookComments.addEventListener("click", showComments);
bookAddComment.addEventListener("click", showAddComment);

//----------------------------------------------------------------
// DOM manipulation procedures

// Procedure to show the book description on user book details page

function showDescription(event) {
    bookDescription.classList.add("active");
    bookStatistics.classList.remove("active");
    bookComments.classList.remove("active");
    bookAddComment.classList.remove("active");
    divDescription.hidden = false;
    divStatistics.hidden = true;
    divComments.hidden = true;
    divAddComment.hidden = true;
}
function showStatistics(event) {
    bookDescription.classList.remove("active");
    bookStatistics.classList.add("active");
    bookComments.classList.remove("active");
    bookAddComment.classList.remove("active");
    divDescription.hidden = true;
    divStatistics.hidden = false;
    divComments.hidden = true;
    divAddComment.hidden = true;
}
function showComments(event) {
    bookDescription.classList.remove("active");
    bookStatistics.classList.remove("active");
    bookComments.classList.add("active");
    bookAddComment.classList.remove("active");
    divDescription.hidden = true;
    divStatistics.hidden = true;
    divComments.hidden = false;
    divAddComment.hidden = true;
}
function showAddComment(event) {
    bookDescription.classList.remove("active");
    bookStatistics.classList.remove("active");
    bookComments.classList.remove("active");
    bookAddComment.classList.add("active");
    divDescription.hidden = true;
    divStatistics.hidden = true;
    divComments.hidden = true;
    divAddComment.hidden = false;
}
