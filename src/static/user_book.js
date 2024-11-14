/*
Title: The BookWormDen
Author: Fabricio Ribeiro
Date: October 6th, 2024
Description: This file handles user page and details for the books in the user reading list.
*/

//global variables

const bookDescription = document.querySelector("#book-description");
const bookStatistics = document.querySelector("#book-statistics");
const bookComments = document.querySelector("#book-comments");
const bookAddComment = document.querySelector("#book-addcomment");
const divDescription = document.querySelector("#div-description");
const divStatistics = document.querySelector("#div-statistics");
const divComments = document.querySelector("#div-comments");
const listComments = document.querySelector("#ul-comments");
const divAddComment = document.querySelector("#div-addcomment");

//================================================================
//Supporting Functions

function getCommentMarkup(comment) {
    return `
        <div class="row">
          <div class="story-data">
            <p>
            ${comment["comment"]}
            </p>
          </div>
          <div class="row">
            <small class="col">by ${comment["username"]}</small>
            <small class="col">Rating: ${comment["rating"]}</small>
            <small class="col">posted on ${comment["date"]}</small>
          </div>
        </div>
        </li>
      `;
}

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
async function showComments(event) {
    bookDescription.classList.remove("active");
    bookStatistics.classList.remove("active");
    bookComments.classList.add("active");
    bookAddComment.classList.remove("active");
    divDescription.hidden = true;
    divStatistics.hidden = true;
    divComments.hidden = false;
    divAddComment.hidden = true;
    const bookId = event.target.dataset.book;
    const commentsList = await Comment.getAllComments(bookId);
    if (!commentsList) {
        listComments.innerHTML = "";
        new_line = document.createElement("p");
        new_line.style.color = "red";
        new_line.innerText =
            "Error reading comments from server, please try again";
        listComments.appendChild(new_line);
    } else {
        listComments.innerHTML = "";
        commentsList.forEach((comment) => {
            const htmlComment = getCommentMarkup(comment);
            const commentEntry = document.createElement("li");
            commentEntry.id = `(${comment.user_id},${comment.bok_id})`;
            commentEntry.classList.add("list-group-item");
            commentEntry.innerHTML = htmlComment;
            listComments.appendChild(commentEntry);
        });
    }
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
