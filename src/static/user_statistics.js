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
    console.log("test");
}
function showStatistics(event) {
    console.log("test");
}
function showComments(event) {
    console.log("test");
}
function showAddComment(event) {
    console.log("test");
}
