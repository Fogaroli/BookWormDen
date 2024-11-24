module.exports = {
    testEnvironment: "jsdom",
    setupFilesAfterEnv: ["<rootDir>/jest.setup.js"],
    moduleDirectories: ["node_modules"],
    moduleFileExtensions: ["js", "jsx"],
    testMatch: ["**/*.test.js"],
    verbose: true,
};
