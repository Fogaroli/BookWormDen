/*
Title: The BookwormDen
Author: Fabricio Ribeiro
Date: October 6th, 2024
Description: This file handles user page and details for the books in the user reading list.
*/

//global variables

const bookDescription = document.querySelector("#book-description");
const bookStatistics = document.querySelector("#book-statistics");
const bookComments = document.querySelector("#book-comments");
const bookAddComment = document.querySelector("#book-add-comment");
const bookClubs = document.querySelector("#book-clubs");
const divDescription = document.querySelector("#div-description");
const divStatistics = document.querySelector("#div-statistics");
const divComments = document.querySelector("#div-comments");
const listComments = document.querySelector("#ul-comments");
const divAddComment = document.querySelector("#div-add-comment");
const divBookClubs = document.querySelector("#div-book-clubs");
const listClubs = document.querySelector("#ul-clubs");
const clubSelectList = document.querySelector("#club-select-list");
const addReadingClubButton = document.querySelector("#add-reading-club");

//================================================================
//Supporting Functions

// Function to generate html markup for book comments
function getCommentMarkup(comment) {
    return `
        <div class="row">
          <div class="story-data">
            <p>
            ${comment["comment"]}
            </p>
          </div>
          <div class="row">
            <small class="col-12 col-lg-4">by ${comment["username"]}</small>
            <small class="col-12 col-lg-4">Rating: ${comment["rating"]}</small>
            <small class="col-12 col-lg-4">posted on ${comment["date"]}</small>
          </div>
        </div>
        </li>
      `;
}

// Function to create li element with reading club name
function getClubLi(clubName) {
    newLi = document.createElement("li");
    newLi.classList.add("list-group-item");
    newLi.innerText = clubName;
    return newLi;
}

// Function to send request to the backend to add book to a new reading club
async function addClub(club, bookId) {
    const response = await axios({
        url: `/book/${bookId}/add`,
        method: "Post",
        data: { club_name: club },
    }).catch((error) => {
        return error;
    });
    if (response instanceof Error) {
        return false;
    }
    return true;
}

//================================================================
//DOM Manipulation

//----------------------------------------------------------------
// Event Listeners

// Event Listener for tab navigation
bookDescription.addEventListener("click", showDescription);
bookStatistics.addEventListener("click", showStatistics);
bookComments.addEventListener("click", showComments);
bookAddComment.addEventListener("click", showAddComment);
bookClubs.addEventListener("click", showBookClubs);

// Event Listener to add book to a reading club
addReadingClubButton.addEventListener("click", addReadingClub);

//----------------------------------------------------------------
// DOM manipulation procedures

// Procedure to process opening the description tab
function showDescription(event) {
    bookDescription.classList.add("active");
    bookStatistics.classList.remove("active");
    bookComments.classList.remove("active");
    bookAddComment.classList.remove("active");
    bookClubs.classList.remove("active");
    divDescription.hidden = false;
    divStatistics.hidden = true;
    divComments.hidden = true;
    divAddComment.hidden = true;
    divBookClubs.hidden = true;
}

// Procedure to process opening the statistics tab
function showStatistics(event) {
    bookDescription.classList.remove("active");
    bookStatistics.classList.add("active");
    bookComments.classList.remove("active");
    bookAddComment.classList.remove("active");
    bookClubs.classList.remove("active");
    divDescription.hidden = true;
    divStatistics.hidden = false;
    divComments.hidden = true;
    divAddComment.hidden = true;
    divBookClubs.hidden = true;
}

// Procedure to process opening the commments tab
async function showComments(event) {
    bookDescription.classList.remove("active");
    bookStatistics.classList.remove("active");
    bookComments.classList.add("active");
    bookAddComment.classList.remove("active");
    bookClubs.classList.remove("active");
    divDescription.hidden = true;
    divStatistics.hidden = true;
    divComments.hidden = false;
    divAddComment.hidden = true;
    divBookClubs.hidden = true;
    const bookId = event.target.dataset.book;
    const commentsList = await Comment.getAllComments(bookId);
    if (!commentsList) {
        listComments.innerHTML = "";
        const newLine = document.createElement("p");
        newLine.innerText = "No comments found in the server.";
        listComments.appendChild(newLine);
    } else {
        listComments.innerHTML = "";
        commentsList.forEach((comment) => {
            const htmlComment = getCommentMarkup(comment);
            const commentEntry = document.createElement("li");
            commentEntry.id = `(${comment.user_id},${comment.book_id})`;
            commentEntry.classList.add("list-group-item");
            commentEntry.innerHTML = htmlComment;
            listComments.appendChild(commentEntry);
        });
    }
}

// Procedure to process opening the tab to add a new comment/ update comment
function showAddComment(event) {
    bookDescription.classList.remove("active");
    bookStatistics.classList.remove("active");
    bookComments.classList.remove("active");
    bookAddComment.classList.add("active");
    bookClubs.classList.remove("active");
    divDescription.hidden = true;
    divStatistics.hidden = true;
    divComments.hidden = true;
    divAddComment.hidden = false;
    divBookClubs.hidden = true;
}

// Procedure to process opening the book clubs tab
async function showBookClubs(event) {
    bookDescription.classList.remove("active");
    bookStatistics.classList.remove("active");
    bookComments.classList.remove("active");
    bookAddComment.classList.remove("active");
    bookClubs.classList.add("active");
    divDescription.hidden = true;
    divStatistics.hidden = true;
    divComments.hidden = true;
    divAddComment.hidden = true;
    divBookClubs.hidden = false;
    const bookId = event.target.dataset.book;
    const clubsMap = await Club.getMemberClubs(bookId);
    listClubs.innerHTML = "";
    clubSelectList.innerHTML = "";
    clubsMap.included.forEach((club) => {
        const newLi = getClubLi(club.name);
        listClubs.appendChild(newLi);
    });
    clubsMap.choices.forEach((club) => {
        newOption = document.createElement("option");
        newOption.value = club.name;
        newOption.innerText = club.name;
        clubSelectList.appendChild(newOption);
    });
}

// Procedure to add the book to a new reading club
async function addReadingClub(event) {
    const bookId = event.target.dataset.book;
    club = clubSelectList.value;
    if (club !== "") {
        const added = await addClub(club, bookId);
        if (added) {
            const newLi = getClubLi(club);
            listClubs.appendChild(newLi);
            option = document.querySelector(`option[value="${club}"]`);
            option.remove();
        }
    }
}

//================================================================
//Setup for unit testing

if (typeof module !== "undefined" && module.exports) {
    module.exports = {
        getCommentMarkup,
        getClubLi,
        addClub,
        showDescription,
        showStatistics,
        showComments,
        showAddComment,
        showBookClubs,
        addReadingClub,
    };
}
