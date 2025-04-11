module.exports = {
    preset: "ts-jest",
    testEnvironment: "node",
    transform: {
        "^.+\\.(ts|tsx)$": "ts-jest"
    },
    moduleFileExtensions: ["ts", "tsx", "js"],
    roots: ["<rootDir>/tests"],
    testMatch: ["**/!(dist)/**/?(*.)+(test|spec).(ts|tsx|js)"]
};