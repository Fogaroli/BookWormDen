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

function getClubLi(club_name) {
    new_li = document.createElement("li");
    new_li.classList.add("list-group-item");
    new_li.innerText = club_name;
    return new_li;
}

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
//Event Listeners

bookDescription.addEventListener("click", showDescription);
bookStatistics.addEventListener("click", showStatistics);
bookComments.addEventListener("click", showComments);
bookAddComment.addEventListener("click", showAddComment);
bookClubs.addEventListener("click", showBookClubs);
addReadingClubButton.addEventListener("click", addReadingClub);

//----------------------------------------------------------------
// DOM manipulation procedures

// Procedure to show the book description on user book details page

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
        new_line = document.createElement("p");
        new_line.innerText = "No comments found in teh server.";
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
    bookClubs.classList.remove("active");
    divDescription.hidden = true;
    divStatistics.hidden = true;
    divComments.hidden = true;
    divAddComment.hidden = false;
    divBookClubs.hidden = true;
}
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
        const new_li = getClubLi(club.name);
        listClubs.appendChild(new_li);
    });
    clubsMap.choices.forEach((club) => {
        new_option = document.createElement("option");
        new_option.value = club.name;
        new_option.innerText = club.name;
        clubSelectList.appendChild(new_option);
    });
}

async function addReadingClub(event) {
    const bookId = event.target.dataset.book;
    club = clubSelectList.value;
    const added = await addClub(club, bookId);
    if (added) {
        const new_li = getClubLi(club);
        listClubs.appendChild(new_li);
        option = document.querySelector(`option[value="${club}"]`);
        console.log(option);
        option.remove();
    }
}
