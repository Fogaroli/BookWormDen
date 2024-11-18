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

function getMessageMarkup(message) {
    const messageEntry = `
        <div class="row">
            <div class="col-1 d-flex justify-content-center align-items-center">
            ${
                userUsername === message["user_username"]
                    ? '<i class="fa-solid fa-burst m-1" title="Remove message"></i>'
                    : ""
            }
            </div>
            <div class="col-11">
                <div class="row">
                    <div class="col">${message["message"]}</div>
                </div>
                <div class="row justify-content-evenly">
                    <div class="col-3">
                        <small>${message["user_first_name"]} ${
        message["user_last_name"]
    }</small>
                    </div>
                    <div class="col-3">
                        <small>${message["timestamp"]}</small>
                    </div>
                </div>
            </div>
        </div>
    `;
    return $("<li>", { class: "list-group-item" }).html(messageEntry);
}

//================================================================
//DOM Manipulation

//----------------------------------------------------------------
//Event Listeners

$sendMessageButton.on("click", sendNewMessage);

$(document).ready(() => {
    loadMessagesOnStartup();
});

//----------------------------------------------------------------
// DOM manipulation procedures

//procedure to load forum messages on startup (load first 20 messages)
async function loadMessagesOnStartup() {
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

//Procedure to add a new message to the forum.
async function sendNewMessage() {
    const messageContent = $newMessageContent.val();
    const message = await Message.sendNewMessage(club_id, messageContent);
    if (message) {
        loadMessagesOnStartup();
    } else {
        const error = $("<small>").text("Error - Fail to send the message");
        $messageForm.append(error);
    }
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
    };
}
