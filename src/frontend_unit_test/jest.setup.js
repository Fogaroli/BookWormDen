const { default: MockAdapter } = require("axios-mock-adapter");
const axios = require("axios");
const $ = require("jquery");
const jestConfig = require("./jest.config");

global.window = global;
global.$ = $;
global.jQuery = $;
global.axios = axios;
global.mockAxios = new MockAdapter(axios);
global.Book = require("../static/book.js");

jest.mock(`axios`);
