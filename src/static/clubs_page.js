/*
Title: The BookWormDen
Author: Fabricio Ribeiro
Date: October 6th, 2024
Description: This file handles user clubs summary page and allow creating new clubs.
*/

//global variables

const addClubButton = document.querySelector("#add-club-btn");
const addClubForm = document.querySelector("#add-club-form");
const errorElements = document.querySelector("[data-error]");

//================================================================
//Supporting Functions

//================================================================
//DOM Manipulation

//----------------------------------------------------------------
//Event Listeners

addClubButton.addEventListener("click", showAddClub);

//----------------------------------------------------------------
// DOM manipulation procedures

// Procedure to show for to add members to the reading club

function showAddClub() {
    addClubForm.hidden = false;
    addClubButton.hidden = true;
}

if (errorElements) {
    showAddClub();
}
