/*
Title: The BookwormDen
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

// clubId = club.id variable injected from backend

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
                    <div class="col fw-bold" id="message-text"></div>
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
    const messageId =
        event.target.parentElement.parentElement.dataset.messageid;
    if (event.target.id === "remove-message") {
        removeMessage(messageId);
    }
    if (event.target.id === "edit-message") {
        showEditMessage(messageId);
    }
}

//================================================================
//DOM Manipulation

//----------------------------------------------------------------
//Event Listeners

// Event listener to monitor the button to send a new message
$sendMessageButton.on("click", sendNewMessage);

// Event listener to process user click to delete or edit a message
$messagesUl.on("click", processMessageIcon);

// Event listener to process the forum messages once the page load is complete
$(document).ready(() => {
    loadInitialMessages();
});

//----------------------------------------------------------------
// DOM manipulation procedures

// Procedure to load forum messages on startup (load first 20 messages)
async function loadInitialMessages() {
    $forumMessageLoading.prop("hidden", false);
    $messagesUl.empty();
    const messageList = await Message.getClubMessages(clubId, 0, 20);
    if (messageList) {
        messageList.forEach((message) => {
            const messageContent = getMessageMarkup(message);
            messageContent
                .find("#message-text")
                .text(message["message"])
                .css("white-space", "pre-wrap");
            $messagesUl.append(messageContent);
        });
        $forumMessageLoading.prop("hidden", true);
    }
}

// Procedure to add a new message to the forum.
async function sendNewMessage() {
    const messageContent = $newMessageContent.val();
    const message = await Message.sendNewMessage(clubId, messageContent);
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
async function removeMessage(messageId) {
    const deleted = await Message.sendDelete(clubId, messageId);
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
function showEditMessage(messageId) {
    const $messageDiv = $(`[data-messagecontent=${messageId}]`);
    const formDiv = getMessageEditMarkup($messageDiv.text().trim());
    $messageDiv.empty();
    $messageDiv.append(formDiv);
}

// Procedure to update message content
async function updateMessage(event) {
    const messageInput = event.target.parentElement.firstElementChild;
    const messageDiv = messageInput.parentElement.parentElement;
    const update = await Message.sendUpdate(
        clubId,
        (messageId = messageDiv.dataset.messagecontent),
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
        getMessageMarkup,
        getMessageEditMarkup,
        processMessageIcon,
        loadInitialMessages,
        sendNewMessage,
        removeMessage,
        showEditMessage,
        updateMessage,
    };
}
