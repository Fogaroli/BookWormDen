class Book {
    /**
     * Class to store information about each book obtained from API.
     * Requests from frontend are managed by the backend, which provides data from search topics.
     */
    constructor(properties) {
        Object.assign(this, { ...properties });
    }

    static async getBookByTitle(titleString){
        /**Class method to get a book list based on the book title. Title sent as parameter */
        const response = await axios({
            url:`/search?q=${titleString}`,
            method: "GET",
        }).catch((error) => {
            return error;
        });
        if (response instanceof Error){
            return;
        }        
        return response.data.map((bookVolume) => new Book(bookVolume["data"]))
    }

    static async getBookDetailById(bookId){
        /**Class method to get book details for a specific book ID, ID provided as parameter */
        const response = await axios({
            url:`/book/${bookId}`,
            method: "GET",
        }).catch((error) => {
            return error;
        });
        if (response instanceof Error){
            return;
        }        
        return new Book(response.data)
    }


}