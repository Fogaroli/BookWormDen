const fs = require("fs");
const path = require("path");

// Import functions to test
const {
    getCommentMarkup,
    getClubLi,
    addClub,
    showDescription,
    showStatistics,
    showComments,
    showAddComment,
    showBookClubs,
    addReadingClub,
} = require("../static/book.js");

beforeEach(() => {
    // Reset mocks and DOM
    global.mockAxios.reset();
    const htmlTemplate = fs.readFileSync(
        path.resolve(__dirname, "../templates/book.html"),
        "utf-8"
    );
    document.body.innerHTML = htmlTemplate;
    // document.dispatchEvent(new Event("DOMContentLoaded"));
});

// Test getCommentMarkup
test("getCommentMarkup generates correct HTML", () => {
    const comment = {
        comment: "Great book!",
        username: "user123",
        rating: 5,
        date: "2024-11-24",
    };

    const html = getCommentMarkup(comment);

    expect(html).toContain("Great book!");
    expect(html).toContain("user123");
    expect(html).toContain("Rating: 5");
    expect(html).toContain("2024-11-24");
});

// // Test getClubLi
// test("getClubLi creates an li element with the club name", () => {
//     const clubName = "Sci-Fi Lovers";
//     const li = getClubLi(clubName);

//     expect(li.tagName).toBe("LI");
//     expect(li.textContent).toBe(clubName);
//     expect(li.classList.contains("list-group-item")).toBe(true);
// });

// // Test addClub
// test("addClub sends request to backend and handles response", async () => {
//     mockAxios.onPost("/book/1/add").reply(200, {});

//     const result = await addClub("Sci-Fi Lovers", 1);

//     expect(result).toBe(true);
//     expect(mockAxios.history.post.length).toBe(1);
//     expect(JSON.parse(mockAxios.history.post[0].data)).toEqual({
//         club_name: "Sci-Fi Lovers",
//     });
// });

// // Test tab navigation
// test("showDescription updates DOM to show description tab", () => {
//     showDescription();

//     expect(
//         document.querySelector("#book-description").classList.contains("active")
//     ).toBe(true);
//     expect(document.querySelector("#div-description").hidden).toBe(false);
//     expect(document.querySelector("#div-statistics").hidden).toBe(true);
// });

// test("showStatistics updates DOM to show statistics tab", () => {
//     showStatistics();

//     expect(
//         document.querySelector("#book-statistics").classList.contains("active")
//     ).toBe(true);
//     expect(document.querySelector("#div-statistics").hidden).toBe(false);
//     expect(document.querySelector("#div-description").hidden).toBe(true);
// });

// // Test showComments
// test("showComments fetches and displays comments", async () => {
//     const mockComments = [
//         {
//             comment: "Great book!",
//             username: "user123",
//             rating: 5,
//             date: "2024-11-24",
//             user_id: 1,
//             book_id: 1,
//         },
//     ];

//     Comment.getAllComments.mockResolvedValue(mockComments);

//     await showComments({ target: { dataset: { book: 1 } } });

//     const commentList = document.querySelector("#ul-comments");
//     expect(commentList.children.length).toBe(1);
//     expect(commentList.innerHTML).toContain("Great book!");
//     expect(commentList.innerHTML).toContain("user123");
// });

// // Test addReadingClub
// test("addReadingClub adds a book to a club and updates DOM", async () => {
//     mockAxios.onPost("/book/1/add").reply(200, {});

//     document.querySelector("#club-select-list").innerHTML = `
//         <option value="Sci-Fi Lovers">Sci-Fi Lovers</option>
//     `;

//     await addReadingClub({ target: { dataset: { book: 1 } } });

//     const listClubs = document.querySelector("#ul-clubs");
//     expect(listClubs.children.length).toBe(1);
//     expect(listClubs.innerHTML).toContain("Sci-Fi Lovers");

//     const clubOption = document.querySelector("#club-select-list option");
//     expect(clubOption).toBeNull();
// });
