import { ReactionHandler } from "../../src/controllers/reaction.controller";
import { Request, Response } from "express";
import axios from "axios";

// Mock axios to prevent real HTTP calls during test
jest.mock("axios");
const mockedAxios = axios as jest.Mocked<typeof axios>;

describe("ReactionHandler.handleReaction", () => {
  let req: Partial<Request>;
  let res: Partial<Response>;

  beforeEach(() => {
    // Set up default request and response mocks
    req = {
      body: {
        songId: "123",
        action: "like",
        userId: "user_abc"
      }
    };

    res = {
      status: jest.fn().mockReturnThis(), // Enables chaining like res.status(400).json(...)
      json: jest.fn()
    };
  });

  // Test Case 1: Missing required input data
  it("should return 400 if any required field is missing", async () => {
    req.body = { songId: "", action: "", userId: "" }; // Simulate empty input

    await ReactionHandler.handleReaction(req as Request, res as Response);

    expect(res.status).toHaveBeenCalledWith(400);
    expect(res.json).toHaveBeenCalledWith({ error: "Missing data" });
  });

  // Test Case 2: Successful reaction post
  it("should call axios and return 200 on success", async () => {
    // Simulate API success response
    mockedAxios.post.mockResolvedValueOnce({
      data: {},
      status: 200,
      statusText: "OK",
      headers: {},
      config: { url: "" }
    });

    await ReactionHandler.handleReaction(req as Request, res as Response);

    // Check axios call is made with correct payload
    expect(mockedAxios.post).toHaveBeenCalledWith(
      expect.stringContaining("/api/update-song"),
      {
        songId: "123",
        action: "like",
        userId: "user_abc"
      }
    );

    // Confirm success response
    expect(res.status).toHaveBeenCalledWith(200);
    expect(res.json).toHaveBeenCalledWith({ success: "Successfully updated song" });
  });

  // Test Case 3: Axios throws an error
  it("should handle axios errors and return 400", async () => {
    // Simulate request failure
    mockedAxios.post.mockRejectedValueOnce(new Error("Request failed"));

    await ReactionHandler.handleReaction(req as Request, res as Response);

    // Confirm error response is handled gracefully
    expect(res.status).toHaveBeenCalledWith(400);
    expect(res.json).toHaveBeenCalledWith({ error: expect.any(Error) });
  });
});
