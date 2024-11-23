const fs = require("fs");
const path = require("path");

const {
    addMarkup,
    starRating,
    addBookDetailsMarkup,
    convertSearchString,
    updateBookSearch,
    showBookDetails,
} = require("../static/app.js");

describe("BookwormDen Frontend Functions", () => {
    beforeEach(() => {
        const htmlTemplate = fs.readFileSync(
            path.resolve(__dirname, "../templates/base.html"),
            "utf-8"
        );
        document.body.innerHTML = htmlTemplate;
        jest.clearAllMocks();
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
            thumbnail: "/mock-thumbnail.jpg",
            publishedDate: "2022",
            description: "This is a mock description.",
        };
        const result = addMarkup(book).prop("outerHTML");
        expect(result).toContain("Mock Book");
        expect(result).toContain("Mock Author");
        expect(result).toContain("/mock-thumbnail.jpg");
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

        const markup = addBookDetailsMarkup(book);
        expect(markup.find("img").attr("src")).toBe("test-url.jpg");
        expect(markup.html()).toContain("Test Publisher");
        expect(markup.html()).toContain("200 pages");
        expect(markup.html()).toContain("Fiction");
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

        // Mock the API response for Axios
        axios.mockResolvedValue({ data: bookList });
        await updateBookSearch(searchInput);

        const searchResultContent = $("#book-search-results").html();
        expect(searchResultContent).toContain("Test Book");
        expect(searchResultContent).toContain("Author One");
    });
});
