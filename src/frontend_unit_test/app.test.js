const fs = require("fs");
const path = require("path");

const {
    addMarkup,
    starRating,
    addBookDetailsMarkup,
    convertSearchString,
    updateBookSearch,
    showBookDetails,
    setBookListeners,
} = require("../static/app.js");

describe("BookwormDen Frontend Functions", () => {
    beforeEach(() => {
        jest.clearAllMocks();
        global.mockAxios.reset();
        const htmlTemplate = fs.readFileSync(
            path.resolve(__dirname, "../templates/base.html"),
            "utf-8"
        );
        document.body.innerHTML = htmlTemplate;
    });

    afterEach(() => {
        jest.resetAllMocks();
        document.body.innerHTML = "";
    });

    test("addMarkup should generate correct HTML for a book", () => {
        const book = {
            id: "1",
            title: "Mock Book",
            authors: "Mock Author",
            thumbnail: "https://example.com/cover.jpg",
            publishedDate: "2022",
            description: "This is a mock description.",
        };
        const fragment = addMarkup(book);
        const element = fragment.children[0];
        const result = element.outerHTML;
        expect(result).toContain("Mock Book");
        expect(result).toContain("Mock Author");
        expect(result).toContain("https://example.com/cover.jpg");
        expect(result).toContain("2022");
    });

    test("starRating should generate the correct number of filled and empty stars", () => {
        const rating3 = starRating(3);
        expect(rating3).toContain("fas fa-star");
        expect(rating3).toContain("far fa-star");
        expect(rating3.match(/fas fa-star/g)).toHaveLength(3);
        expect(rating3.match(/far fa-star/g)).toHaveLength(2);
    });

    test("addBookDetailsMarkup generates correct detail markup", () => {
        const book = {
            id: "123",
            title: "Test Book",
            authors: "Test Author",
            description: "Test Description",
            thumbnail: "test-url.jpg",
            publishedDate: "2024",
            publisher: "Test Publisher",
            page_count: 200,
            average_rating: 4,
            categories: "Fiction",
        };

        const fragment = addBookDetailsMarkup(book);
        const element = fragment.children[0];
        expect(element.querySelector("img").src).toBe("test-url.jpg");
        expect(element.innerHTML).toContain("Test Publisher");
        expect(element.innerHTML).toContain("200 pages");
        expect(element.innerHTML).toContain("Fiction");
    });

    test("convertSearchString handles quoted strings correctly", () => {
        expect(convertSearchString("hello world")).toBe("hello+world");
        expect(convertSearchString('"hello world"')).toBe('"hello world"');
        expect(convertSearchString('test "quoted phrase" test')).toBe(
            'test+"quoted phrase"+test'
        );
    });

    test("updateBookSearch should add book results on successful API call", async () => {
        const searchInput = "Test Book";

        const bookList = [
            {
                data: {
                    id: "1",
                    title: "Test Book",
                    authors: "Author One",
                    thumbnail: "www.test.com/thumbnail.jpg",
                    publishedDate: "2022",
                    description: "Test description",
                },
            },
        ];
        global.mockAxios
            .onGet("/search", { params: { q: searchInput } })
            .reply(200, bookList);

        await updateBookSearch(searchInput);

        const observer = new MutationObserver((mutations, obs) => {
            const searchResultContent = $("#book-search-results").html();

            if (
                searchResultContent.includes("Test Book") &&
                searchResultContent.includes("Author One")
            ) {
                obs.disconnect();

                expect(searchResultContent).toContain("Test Book");
                expect(searchResultContent).toContain("Author One");
            }
        });

        observer.observe(document.querySelector("#book-search-results"), {
            childList: true,
            subtree: true,
        });
    });

    test("updateBookSearch handles API failure gracefully", async () => {
        const searchInput = "Failing Search";

        global.mockAxios
            .onGet("/search", { params: { q: searchInput } })
            .reply(500);

        await updateBookSearch(searchInput);

        const observer = new MutationObserver((mutations, obs) => {
            const errorMsg = $("#book-search-results").find("p").text();

            if (errorMsg.includes("Error to connect to the search server")) {
                obs.disconnect();

                expect(errorMsg).toBe(
                    "Error to connect to the search server, please try again."
                );
            }
        });

        observer.observe(document.querySelector("#book-search-results"), {
            childList: true,
            subtree: true,
        });
    });

    test("setBookListeners attaches event listeners correctly", () => {
        document.body.innerHTML = `
            <ul id="book-search-results">
                <li>
                    <strong class="book-link" id="1">Book Title</strong>
                    <img class="book-cover-image" id="1" src="book-cover.jpg" />
                </li>
            </ul>
        `;

        const mockShowBookDetails = jest.fn();
        document.addEventListener = jest.fn();

        setBookListeners();

        $(".book-link").trigger("click");
        $(".book-cover-image").trigger("click");

        expect($(".book-link").length).toBe(1);
        expect($(".book-cover-image").length).toBe(1);
    });

    test("showBookDetails fetches and displays book details correctly", async () => {
        const bookId = "1";
        const mockBookData = {
            id: "1",
            title: "Mock Book",
            authors: "Mock Author",
            thumbnail: "https://example.com/mock.jpg",
            publishedDate: "2023",
            description: "Mock book description",
            publisher: "Mock Publisher",
            page_count: 300,
            average_rating: 4.5,
            categories: "Fiction",
        };

        global.mockAxios.onGet(`/book/${bookId}`).reply(200, mockBookData);

        const mockEvent = { target: { id: bookId } };
        await showBookDetails(mockEvent);

        const observer = new MutationObserver((mutations, obs) => {
            const detailsContent = $("#book-details").html();

            if (detailsContent.includes("Mock Book")) {
                obs.disconnect();
                expect(detailsContent).toContain("Mock Book");
                expect(detailsContent).toContain("Mock Author");
                expect(detailsContent).toContain("Mock Publisher");
                expect(detailsContent).toContain("Fiction");
                expect(detailsContent).toContain("300 pages");
            }
        });

        observer.observe(document.querySelector("#book-search-results"), {
            childList: true,
            subtree: true,
        });
    });

    test("showBookDetails handles API failure correctly", async () => {
        const bookId = "2";

        global.mockAxios.onGet(`/book/${bookId}`).reply(500);

        const mockEvent = { target: { id: bookId } };
        await showBookDetails(mockEvent);

        const observer = new MutationObserver((mutations, obs) => {
            const errorMsg = $("#book-details").find("p").text();

            if (errorMsg.includes("Error to connect to the search server")) {
                obs.disconnect();

                expect(errorMsg).toBe(
                    "Error to connect to the search server, please try again."
                );
            }
        });

        observer.observe(document.querySelector("#book-search-results"), {
            childList: true,
            subtree: true,
        });
    });
});
