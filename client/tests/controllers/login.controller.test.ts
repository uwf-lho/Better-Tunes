import { LoginAccountController } from "../../src/controllers/login.controller";
import { Request, Response } from "express";
import axios from "axios";

// Mock the axios library to avoid making real HTTP requests
jest.mock("axios");
const mockedAxios = axios as jest.Mocked<typeof axios>;

describe("LoginAccountController.loginAccount", () => {
  let req: Partial<Request>;
  let res: Partial<Response>;

  // Set up a new mock request and response object before each test
  beforeEach(() => {
    req = {
      body: {
        username: "testuser",
        password: "testpass"
      },
      session: {
        user: undefined
      } as any, // Avoids TypeScript errors for incomplete session
      flash: jest.fn() // Mock flash messaging
    };

    res = {
      redirect: jest.fn() // Mock redirect
    };
  });

  // Test Case 1: Missing username or password
  it("should redirect to /login if username or password is missing", async () => {
    req.body = { username: "", password: "" }; // Simulate empty form submission

    await LoginAccountController.loginAccount(req as Request, res as Response);

    expect(req.flash).toHaveBeenCalledWith("error", "Please fill in all fields.");
    expect(res.redirect).toHaveBeenCalledWith("/login");
  });

  // Test Case 2: Successful login and redirect to dashboard
  it("should call API and redirect to /dashboard on success", async () => {
    // Simulate a successful response from the backend API
    mockedAxios.post.mockResolvedValueOnce({
      data: {
        access_token: "fake-token"
      },
      status: 200,
      statusText: "OK",
      headers: {},
      config: { url: "" },
    });

    await LoginAccountController.loginAccount(req as Request, res as Response);

    // Confirm correct API call
    expect(mockedAxios.post).toHaveBeenCalledWith(
      expect.stringContaining("/auth/login"),
      {
        username: "testuser",
        password: "testpass"
      }
    );

    // Confirm session was updated
    expect(req.session!.user).toEqual({
      username: "testuser",
      token: "fake-token"
    });

    // Confirm redirection to dashboard
    expect(res.redirect).toHaveBeenCalledWith("/dashboard");
  });

  // Test Case 3: Known login error with API-provided message
  it("should handle login errors and redirect to /login with flash message", async () => {
    mockedAxios.post.mockRejectedValueOnce({
      response: {
        data: {
          msg: "Invalid credentials"
        }
      }
    });

    await LoginAccountController.loginAccount(req as Request, res as Response);

    // Confirm proper error handling and redirection
    expect(req.flash).toHaveBeenCalledWith("error", "Invalid credentials");
    expect(res.redirect).toHaveBeenCalledWith("/login");
  });

  // Test Case 4: Unknown error response (no msg)
  it("should handle unknown login errors with generic message", async () => {
    mockedAxios.post.mockRejectedValueOnce({}); // Simulate unexpected error shape

    await LoginAccountController.loginAccount(req as Request, res as Response);

    expect(req.flash).toHaveBeenCalledWith("error", "Something went wrong. Please try again later.");
    expect(res.redirect).toHaveBeenCalledWith("/login");
  });
});
