/*
Title: The BookWormDen
Author: Fabricio Ribeiro
Date: October 6th, 2024
Description: This file contains the comments class to handle book feedback recorded by users.
*/

class Comment {
    /**
     * Class to store book comments information.
     * Requests from frontend are managed by the backend, which book comments stores in the database.
     */
    constructor(properties) {
        Object.assign(this, { ...properties });
    }

    static async getAllComments(volume_id) {
        /**Class method to get all available comments for a given book */
        const response = await axios({
            url: `/comments/${volume_id}`,
            method: "GET",
        }).catch((error) => {
            return error;
        });
        if (response instanceof Error) {
            return;
        }
        return response.data.comments.map((comment) => new Comment(comment));
    }
}

//================================================================
//Setup for unit testing
if (typeof module !== "undefined" && module.exports) {
    module.exports = Comment;
}
