const { default: MockAdapter } = require("axios-mock-adapter");
const axios = require("axios");
const $ = require("jquery");

global.window = global;
global.$ = $;
global.jQuery = $;
global.axios = axios;
global.mockAxios = new MockAdapter(axios);
jest.mock(`axios`);

const { Book, Comment, Club, Message } = require("../static/classes.js");
global.Book = Book;
global.Comment = Comment;
global.Club = Club;
global.Message = Message;
