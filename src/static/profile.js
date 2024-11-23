/*
Title: The BookwormDen
Author: Fabricio Ribeiro
Date: October 6th, 2024
Description: This file handles user sign, login and info edit pages.
*/

//global variables

const signupForm = document.querySelector("#signup_form");

const editUserButton = document.querySelector("#edit-user-btn");
const updatePasswordButton = document.querySelector("#update-password-btn");
const profileDiv = document.querySelector("#show-profile");
const editDiv = document.querySelector("#edit-form");
const passwordChangeDiv = document.querySelector("#password-change");

const validateDigit = document.querySelector("#validate-digits");
const validateUppercase = document.querySelector("#validate-uppercase");
const validateLowercase = document.querySelector("#validate-lowercase");
const validateNumeric = document.querySelector("#validate-numeric");

const errorFormElements = document.querySelector("[data-error]");
const errorPasswordElements = document.querySelector("[data-error-password]");

//================================================================
//Supporting Functions

//================================================================
//DOM Manipulation

//----------------------------------------------------------------
//Event Listeners

// Event listener to monitor input entries in the password field and update visual cues to meet password requirements.
if (signupForm) {
    $("#password").on("input", updateValidators);
}

// Event listener to monitor button to edit user information
if (editDiv) {
    editUserButton.addEventListener("click", showEditForm);
}

// Event listener to monitor button to change password
if (passwordChangeDiv) {
    updatePasswordButton.addEventListener("click", showUpdatePasswordForm);
}

// Event listener to monitor input entries in the password change field and update visual cues to meet password requirements.
if (passwordChangeDiv) {
    $("#new_password").on("input", updateValidators);
}

//----------------------------------------------------------------
// DOM manipulation procedures

// Procedure to show user information edit form
function showEditForm() {
    profileDiv.hidden = true;
    editDiv.hidden = false;
}

// Procedure to show password change form
function showUpdatePasswordForm() {
    profileDiv.hidden = true;
    passwordChangeDiv.hidden = false;
}

// Procedure to toggle the password validators indicators
function updateValidators() {
    const input = $(this).val();
    if (/[A-Z]/.test(input)) {
        validateUppercase.classList.remove("text-secondary");
        validateUppercase.classList.add("text-success");
    } else {
        validateUppercase.classList.add("text-secondary");
        validateUppercase.classList.remove("text-success");
    }
    if (/[a-z]/.test(input)) {
        validateLowercase.classList.remove("text-secondary");
        validateLowercase.classList.add("text-success");
    } else {
        validateLowercase.classList.add("text-secondary");
        validateLowercase.classList.remove("text-success");
    }
    if (/[0-9]/.test(input)) {
        validateNumeric.classList.remove("text-secondary");
        validateNumeric.classList.add("text-success");
    } else {
        validateNumeric.classList.add("text-secondary");
        validateNumeric.classList.remove("text-success");
    }
    if (/.{6,}/.test(input)) {
        validateDigit.classList.remove("text-secondary");
        validateDigit.classList.add("text-success");
    } else {
        validateDigit.classList.add("text-secondary");
        validateDigit.classList.remove("text-success");
    }
}

// Show user information edit form in case or form validation error
if (errorFormElements) {
    showEditForm();
}

// show password change form in case of form validation error
if (errorPasswordElements) {
    showUpdatePasswordForm();
}
