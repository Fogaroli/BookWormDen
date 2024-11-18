/*
Title: The BookWormDen
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

// club_id = club.id variable injected from backend

//================================================================
//Supporting Functions

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

async function sendDeleteBook(book_id, club_id) {
    const response = await axios({
        url: `/book/${book_id}/delete`,
        method: "Post",
        data: { club_id: club_id },
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

if (addMemberButton) {
    addMemberButton.addEventListener("click", showAddMember);
}

deleteMemberButton.forEach((button) => {
    button.addEventListener("click", deleteMember);
});
deleteBookButton.forEach((button) => {
    button.addEventListener("click", deleteBook);
});
sendInviteButton.addEventListener("click", addMember);
userSearchInput.addEventListener("input", showDropdown);

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

async function showDropdown() {
    const q = userSearchInput.value;
    users = await searchUser(q);
    if (users) {
        userDropdown.innerHTML = "";
        users.forEach((user) => {
            const new_entry = document.createElement("div");
            new_entry.classList.add("dropdown-item");
            new_entry.textContent = user;
            new_entry.addEventListener("click", () => {
                userSearchInput.value = user;
                userDropdown.innerHTML = "";
            });
            userDropdown.appendChild(new_entry);
        });
        userDropdown.hidden = users.length ? false : true;
    } else {
        userDropdown.innerHTML = "";
        userDropdown.hidden = true;
    }
}

async function addMember() {
    if (
        userSearchInput.value.length > 0 &&
        userSearchInput.value !== "ERROR - Try Again"
    ) {
        const inputParts = userSearchInput.value.split("-");
        const username = inputParts[inputParts.length - 1].trim();
        const invite = await sendInvite(club_id, username);
        if (invite) {
            userSearchInput.innerHTML = "";
            new_member_row = document.createElement("div");
            new_member_row.classList.add("row");

            new_member = document.createElement("div");
            new_member.classList.add("col");
            new_member.innerHTML = `${invite.added_member.first_name} ${invite.added_member.last_name}
             <span class='badge text-bg-warning'><i class='fa-solid fa-hourglass-start'></i></span>`;

            excludeIcon = document.createElement("span");
            excludeIcon.classList.add("badge", "text-bg-light");
            excludeIcon.innerHTML = `<i class="fa-solid fa-burst" title="Exclude" data-delete-member-btn data-username="${username}"></i>`;
            excludeIcon.addEventListener("click", deleteMember);

            new_member.appendChild(excludeIcon);
            new_member_row.appendChild(new_member);

            membersListDiv.appendChild(new_member_row);
            userSearchInput.value = "";
        } else {
            userSearchInput.value = "ERROR - Try Again";
        }
    }
}

//procedure to delete user from book club
async function deleteMember(event) {
    const deleted = await sendDeleteMember(
        club_id,
        event.target.dataset.username
    );
    if (deleted) {
        userDiv = event.target.closest("div").parentElement;
        userDiv.remove();
    }
}

//procedure to delete book from book club reading list
async function deleteBook(event) {
    const deleted = await sendDeleteBook(event.target.dataset.book, club_id);
    if (deleted) {
        bookDiv = event.target.closest("div").parentElement;
        bookDiv.remove();
    }
}
