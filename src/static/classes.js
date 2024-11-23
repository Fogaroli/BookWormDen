/*
Title: The BookwormDen
Author: Fabricio Ribeiro
Date: October 6th, 2024
Description: This file contains the javascript classes used in the project. This is accessed by multiple scripts.
*/

class Book {
    /**
     * Class to store information about each book obtained from API.
     * Requests from frontend are managed by the backend, which provides data from search topics.
     */
    constructor(properties) {
        Object.assign(this, { ...properties });
    }

    static async getBookByTitle(titleString) {
        /**Class method to get a book list based on the book title. Title sent as parameter */
        const response = await axios
            .get(`/search`, {
                params: { q: titleString },
            })
            .catch((error) => {
                return error;
            });
        if (response instanceof Error) {
            return;
        }
        return response.data.map((bookVolume) => new Book(bookVolume["data"]));
    }

    static async getBookDetailById(bookId) {
        /**Class method to get book details for a specific book ID, ID provided as parameter */
        const response = await axios.get(`/book/${bookId}`).catch((error) => {
            return error;
        });
        if (response instanceof Error) {
            return;
        }
        return new Book(response.data);
    }
}

class Comment {
    /**
     * Class to store book comments information.
     * Requests from frontend are managed by the backend, which book comments stores in the database.
     */
    constructor(properties) {
        Object.assign(this, { ...properties });
    }

    static async getAllComments(volumeId) {
        /**Class method to get all available comments for a given book */
        const response = await axios
            .get(`/comments/${volumeId}`)
            .catch((error) => {
                return error;
            });
        if (response instanceof Error) {
            return;
        }
        return response.data.comments.map((comment) => new Comment(comment));
    }
}

class Club {
    /**
     * Class used to store Reading Club information
     */

    constructor(name) {
        this.name = name;
    }

    static async getMemberClubs(volumeId) {
        /**Class method to get all reading clubs a give user is member or owner */

        const response = await axios
            .get(`/book/${volumeId}/clubs`)
            .catch((error) => {
                return error;
            });
        if (response instanceof Error) {
            return;
        }
        const includedClubList = response.data.included.map((name) => {
            return new Club(name);
        });
        const choicesClubList = response.data.choices.map((name) => {
            return new Club(name);
        });
        return { included: includedClubList, choices: choicesClubList };
    }
}

class Message {
    /**
     * Class to store information about each book obtained from API.
     * Requests from frontend are managed by the backend, which provides data from search topics.
     */
    constructor(properties) {
        Object.assign(this, { ...properties });
    }

    static async getClubMessages(clubId, offset, quantity) {
        /**Class method to get club messages from the server*/
        const response = await axios
            .get(`/clubs/${clubId}/messages`, {
                params: { start: offset, quantity: quantity },
            })
            .catch((error) => {
                return error;
            });
        if (response instanceof Error) {
            return false;
        }
        return response.data.messages.map((message) => new Message(message));
        //messages format from server: {id, message, timestamp, user_first_name, user_last_name, user_username}
    }

    static async sendNewMessage(clubId, message) {
        /**Class method to send a new forum message to the server */
        const response = await axios({
            url: `/clubs/${clubId}/messages`,
            method: "POST",
            data: { message: message },
        }).catch((error) => {
            return error;
        });
        if (response instanceof Error) {
            return false;
        }
        return new Message(message);
    }

    static async sendDelete(clubId, messageId) {
        /**Class method to delete a message from the server */
        const response = await axios({
            url: `/clubs/${clubId}/messages/${messageId}`,
            method: "DELETE",
            data: { message: messageId },
        }).catch((error) => {
            return error;
        });
        if (response instanceof Error) {
            return false;
        }
        return true;
    }

    static async sendUpdate(clubId, messageId, message) {
        /**Class method to update a message content from the club forum */
        const response = await axios({
            url: `/clubs/${clubId}/messages/${messageId}`,
            method: "PATCH",
            data: { message: message },
        }).catch((error) => {
            return error;
        });
        if (response instanceof Error) {
            return false;
        }
        return new Message(message);
    }
}

//================================================================
//Setup for unit testing
if (typeof module !== "undefined" && module.exports) {
    module.exports = { Book, Comment, Club, Message };
}
