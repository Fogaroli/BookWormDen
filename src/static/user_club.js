/*
Title: The BookwormDen
Author: Fabricio Ribeiro
Date: October 6th, 2024
Description: This file handles club page with members.
*/

//global variables

const addMemberButton = document.querySelector("#add-member-btn");
const deleteMemberButton = document.querySelectorAll(
    "[data-delete-member-btn]"
);
const sendInviteButton = document.querySelector("#send-invite-btn");
const addMemberForm = document.querySelector("#add-member-form");
const userSearchInput = document.querySelector("#user-input");
const userDropdown = document.querySelector("#user-dropdown-list");
const membersListDiv = document.querySelector("#members-list");
const deleteBookButton = document.querySelectorAll("[data-delete-book-btn]");

// clubId = club.id variable injected from backend

//================================================================
//Supporting Functions

// Function to request a users list to the backend matching the give string
async function searchUser(q) {
    if (q.length > 2) {
        const response = await axios({
            url: `/user/search?q=${q}`,
            method: "Get",
        }).catch((error) => {
            return error;
        });
        if (response instanceof Error) {
            return false;
        }
        return response.data;
    }
}

// Function to request the backend to send a invite to a user to join a reading club
async function sendInvite(club, username) {
    const response = await axios({
        url: `/clubs/${club}/add`,
        method: "Post",
        data: { username: username },
    }).catch((error) => {
        return error;
    });
    if (response instanceof Error) {
        return false;
    }
    return response.data;
}

// Function to send a request to the backend to delete a member from the reading club
async function sendDeleteMember(club, username) {
    const response = await axios({
        url: `/clubs/${club}/delete`,
        method: "Post",
        data: { username: username },
    }).catch((error) => {
        return error;
    });
    if (response instanceof Error) {
        return false;
    }
    return true;
}

// Function to send a request to the backend to remove a book from the reading club
async function sendDeleteBook(bookId, clubId) {
    const response = await axios({
        url: `/book/${bookId}/delete`,
        method: "Post",
        data: { club_id: clubId },
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

// Event listener to process clicks to add a new member
if (addMemberButton) {
    addMemberButton.addEventListener("click", showAddMember);
}

// Event listener to process clicks on the icon to delete a user
deleteMemberButton.forEach((button) => {
    button.addEventListener("click", deleteMember);
});

// Event listener to process clicks on the icon to remove a book from the club
deleteBookButton.forEach((button) => {
    button.addEventListener("click", deleteBook);
});

// Event listener to process request to send a join request to a member
sendInviteButton.addEventListener("click", addMember);

// Event Listener to process inputs in the add member field.
userSearchInput.addEventListener("input", showDropdown);

// Event listener to process clicks outside the user search area to hide the search dropdown
document.addEventListener("click", (event) => {
    if (
        !userDropdown.contains(event.target) &&
        event.target !== userSearchInput
    ) {
        userDropdown.hidden = true;
    }
});

//----------------------------------------------------------------
// DOM manipulation procedures

// Procedure to show for to add members to the reading club
function showAddMember() {
    addMemberForm.hidden = false;
    addMemberButton.hidden = true;
}

// Procedure to show a dropdown box with users matching the input string
async function showDropdown() {
    const q = userSearchInput.value;
    users = await searchUser(q);
    if (users) {
        userDropdown.innerHTML = "";
        users.forEach((user) => {
            const newEntry = document.createElement("div");
            newEntry.classList.add("dropdown-item");
            newEntry.textContent = user;
            newEntry.addEventListener("click", () => {
                userSearchInput.value = user;
                userDropdown.innerHTML = "";
            });
            userDropdown.appendChild(newEntry);
        });
        userDropdown.hidden = users.length ? false : true;
    } else {
        userDropdown.innerHTML = "";
        userDropdown.hidden = true;
    }
}

// Procedure to send a join invite to the selected user
async function addMember() {
    if (
        userSearchInput.value.length > 0 &&
        userSearchInput.value !== "ERROR - Try Again"
    ) {
        const inputParts = userSearchInput.value.split("-");
        const username = inputParts[inputParts.length - 1].trim();
        const invite = await sendInvite(clubId, username);
        if (invite) {
            userSearchInput.innerHTML = "";
            const newMemberRow = document.createElement("div");
            newMemberRow.classList.add("row");

            const newMember = document.createElement("div");
            newMember.classList.add("col");
            newMember.innerHTML = `${invite.added_member.first_name} ${invite.added_member.last_name}
             <span class='badge text-bg-warning'><i class='fa-solid fa-hourglass-start'></i></span>`;

            excludeIcon = document.createElement("span");
            excludeIcon.classList.add("badge", "text-bg-light");
            excludeIcon.innerHTML = `<i class="fa-solid fa-burst" title="Exclude" data-delete-member-btn data-username="${username}"></i>`;
            excludeIcon.addEventListener("click", deleteMember);

            newMember.appendChild(excludeIcon);
            newMemberRow.appendChild(newMember);

            membersListDiv.appendChild(newMemberRow);
            userSearchInput.value = "";
            if (document.querySelector("#error-message")) {
                document.querySelector("#error-message").remove();
            }
        } else {
            const errorMessage = document.createElement("small");
            errorMessage.id = "error-message";
            errorMessage.innerText =
                "Could not find/add user, please confirm name and try again";
            errorMessage.classList.add("text-danger");
            userSearchInput.parentElement.appendChild(errorMessage);
        }
    }
}

//procedure to delete user from book club
async function deleteMember(event) {
    const deleted = await sendDeleteMember(
        clubId,
        event.target.dataset.username
    );
    if (deleted) {
        userDiv = event.target.closest("div").parentElement;
        userDiv.remove();
    }
}

//procedure to delete book from book club reading list
async function deleteBook(event) {
    const deleted = await sendDeleteBook(event.target.dataset.book, clubId);
    if (deleted) {
        bookDiv = event.target.closest("div").parentElement;
        bookDiv.remove();
    }
}

//================================================================
//Setup for unit testing

if (typeof module !== "undefined" && module.exports) {
    module.exports = {
        searchUser,
        sendInvite,
        sendDeleteMember,
        sendDeleteBook,
        showAddMember,
        showDropdown,
        addMember,
        deleteMember,
        deleteBook,
    };
}
