const fs = require("fs");
const path = require("path");
const $ = require('jquery');
const Book = require("../static/book.js");

// Mock the Book class methods
jest.mock('../static/book.js', () => {
  return {
    getBookByTitle: jest.fn(),
    getBookDetailById: jest.fn(),
  };
});