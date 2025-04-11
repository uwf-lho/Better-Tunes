import { SearchController } from "../../src/controllers/search.controller";
import { Request, Response } from "express";
import axios from "axios";

// Mock axios to prevent real HTTP requests during test runs
jest.mock("axios");
const mockedAxios = axios as jest.Mocked<typeof axios>;

describe("SearchController.getResults", () => {
  let req: Partial<Request>;
  let res: Partial<Response>;

  beforeEach(() => {
    // Mocking request and session data
    req = {
      body: {
        "search-input": "guitar",
        "query-type-dropdown": "title"
      },
      session: {
        user: { username: "testuser" }
      } as any,
      flash: jest.fn()
    };

    // Mocking response functions
    res = {
      redirect: jest.fn(),
      render: jest.fn()
    };

    // Suppress console.error output in test logs
    jest.spyOn(console, "error").mockImplementation(() => {});
  });

  // Test Case 1: Missing form fields
  it("should redirect if any field is missing", async () => {
    req.body = { "search-input": "", "query-type-dropdown": "" };

    await SearchController.getResults(req as Request, res as Response);

    expect(req.flash).toHaveBeenCalledWith("error", "Please fill in all fields.");
    expect(res.redirect).toHaveBeenCalledWith("/dashboard");
  });

  // Test Case 2: Successful API response
  it("should call API and render results on success", async () => {
    mockedAxios.post.mockResolvedValueOnce({
      data: [{ title: "Song A" }, { title: "Song B" }],
      status: 200,
      statusText: "OK",
      headers: {},
      config: { url: "" }
    });

    await SearchController.getResults(req as Request, res as Response);

    // Confirm correct API payload
    expect(mockedAxios.post).toHaveBeenCalledWith(
      expect.stringContaining("/api/search"),
      {
        query_type: "title",
        payload: "guitar",
        username: "testuser"
      }
    );

    // Confirm correct rendering of the results page
    expect(res.render).toHaveBeenCalledWith("results", {
      user: { username: "testuser" },
      cards: [{ title: "Song A" }, { title: "Song B" }],
      query_type: "title",
      search_query: "guitar",
      userId: "testuser"
    });
  });

  // Test Case 3: API error with known message
  it("should handle API errors and redirect to /login with flash message", async () => {
    mockedAxios.post.mockRejectedValueOnce({
      response: {
        data: {
          msg: "API error"
        }
      }
    });

    await SearchController.getResults(req as Request, res as Response);

    expect(req.flash).toHaveBeenCalledWith("error", "API error");
    expect(res.redirect).toHaveBeenCalledWith("/login");
  });

  // Test Case 4: Unknown error (malformed or missing response)
  it("should handle unknown errors and show default flash message", async () => {
    mockedAxios.post.mockRejectedValueOnce({}); // Simulate error with no message

    await SearchController.getResults(req as Request, res as Response);

    expect(req.flash).toHaveBeenCalledWith("error", "Something went wrong. Please try again later.");
    expect(res.redirect).toHaveBeenCalledWith("/login");
  });
});
