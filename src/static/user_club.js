/*
Title: The BookWormDen
Author: Fabricio Ribeiro
Date: October 6th, 2024
Description: This file handles club page with members and discussion forum.
*/

//global variables

console.log(users);

const addMemberButton = document.querySelector("#add-member-btn");
const addMemberForm = document.querySelector("#add-member-form");

//================================================================
//Supporting Functions

//================================================================
//DOM Manipulation

//----------------------------------------------------------------
//Event Listeners

addMemberButton.addEventListener("click", showAddMember);

//----------------------------------------------------------------
// DOM manipulation procedures

// Procedure to show for to add members to the reading club
function showAddMember() {
    addMemberForm.hidden = false;
}
