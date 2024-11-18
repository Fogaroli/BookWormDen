/*
Title: The BookWormDen
Author: Fabricio Ribeiro
Date: October 6th, 2024
Description: This file handles the message forum in the reading club.
*/

//global variables

const $messagesUl = $("#club-forum");
const $forumMessageLoading = $("#forum-loading-msg");
const userUsername = $("#user-page-link").text();
const $newMessageContent = $("#new-message-content");
const $sendMessageButton = $("#send-message-btn");
const $messageForm = $("#new-message-form");

// club_id = club.id variable injected from backend

//================================================================
//Supporting Functions

// Function to create a li element with a message text based on the message map provided
function getMessageMarkup(message) {
    const messageEntry = `
        <div class="row" data-messageid=${message.id}>
            <div class="col-1 d-flex justify-content-center align-items-center">
            ${
                userUsername === message["user_username"]
                    ? `<i class="fa-solid fa-burst m-1 action" id="remove-message" title="Remove message"></i>
                    <i class="m-1 fa-regular fa-pen-to-square action" id="edit-message" title="Edit Message"></i>`
                    : ""
            }
            </div>

            <div class="col-3 text-center">
                <p class="fw-bold">${message["user_first_name"]} ${
        message["user_last_name"]
    }</p>
                <small>${message["timestamp"]}</small>
            </div>

            <div class="col-8">
                <div class="row" data-messagecontent=${message.id}>
                    <div class="col fw-bold">${message["message"].replace(
                        /\n/g,
                        "<br>"
                    )}</div>
                </div>
            </div>
        </div>
    `;
    return $("<li>", { class: "list-group-item" }).html(messageEntry);
}

// Function to create the input text area for a message edit. Event listener to handle updates
function getMessageEditMarkup(message) {
    const inputMarkup = `
        <textarea class="form-control" aria-label="edit message input">${message}</textarea>
        <span class="input-group-text btn btn-dark" id="send-update-btn">Update</span>  
    `;
    const newDiv = $("<div>", { class: "input-group mb-3" }).html(inputMarkup);
    newDiv.on("click", (event) => {
        if (event.target.id === "send-update-btn") {
            updateMessage(event);
        }
    });
    return newDiv;
}

// Function to process the event listener for the message action icons, delete and edit
function processMessageIcon(event) {
    const message_id =
        event.target.parentElement.parentElement.dataset.messageid;
    if (event.target.id === "remove-message") {
        removeMessage(message_id);
    }
    if (event.target.id === "edit-message") {
        showEditMessage(message_id);
    }
}

//================================================================
//DOM Manipulation

//----------------------------------------------------------------
//Event Listeners

$sendMessageButton.on("click", sendNewMessage);

$messagesUl.on("click", processMessageIcon);

$(document).ready(() => {
    loadInitialMessages();
});

//----------------------------------------------------------------
// DOM manipulation procedures

// Procedure to load forum messages on startup (load first 20 messages)
async function loadInitialMessages() {
    $forumMessageLoading.prop("hidden", false);
    $messagesUl.empty();
    const messageList = await Message.getClubMessages(club_id, 0, 20);
    if (messageList) {
        messageList.forEach((message) => {
            const messageContent = getMessageMarkup(message);
            $messagesUl.append(messageContent);
        });
        $forumMessageLoading.prop("hidden", true);
    }
}

// Procedure to add a new message to the forum.
async function sendNewMessage() {
    const messageContent = $newMessageContent.val();
    const message = await Message.sendNewMessage(club_id, messageContent);
    if (message) {
        loadInitialMessages();
        $newMessageContent.val("");
    } else {
        const error = $("<small>", { class: "error" }).text(
            "Error - Failed to send the message"
        );
        $messagesUl.prepend(error);
    }
}

// Procedure to delete a message from the forum
async function removeMessage(message_id) {
    const deleted = await Message.sendDelete(club_id, message_id);
    if (deleted) {
        loadInitialMessages();
    } else {
        const error = $("<small>", { class: "error" }).text(
            "Error - Failed to remove message"
        );
        $messagesUl.prepend(error);
    }
}

// Procedure to open an input field to allow message editing
function showEditMessage(message_id) {
    const $messageDiv = $(`[data-messagecontent=${message_id}]`);
    const formDiv = getMessageEditMarkup($messageDiv.text().trim());
    $messageDiv.empty();
    $messageDiv.append(formDiv);
}

// Procedure to update message content
async function updateMessage(event) {
    const messageInput = event.target.parentElement.firstElementChild;
    const messageDiv = messageInput.parentElement.parentElement;
    const update = await Message.sendUpdate(
        club_id,
        (message_id = messageDiv.dataset.messagecontent),
        (message = messageInput.value)
    );
    if (update) {
        loadInitialMessages();
    } else {
        const error = $("<small>", { class: "error" }).text(
            "Error - Failed to update message"
        );
        $messagesUl.prepend(error);
    }
}

//================================================================
// Setup for unit testing

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
