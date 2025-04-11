import { RegisterAccountController } from "../../src/controllers/register.controller";
import { Request, Response } from "express";
import axios from "axios";

// Mock axios so no real HTTP calls are made
jest.mock("axios");
const mockedAxios = axios as jest.Mocked<typeof axios>;

describe("RegisterAccountController.registerAccount", () => {
  let req: Partial<Request>;
  let res: Partial<Response>;

  beforeEach(() => {
    req = {
      body: {
        username: "testuser",
        password: "pass123",
        password2: "pass123"
      },
      session: {
        user: undefined
      } as any, // Prevent TypeScript errors due to missing Session fields
      flash: jest.fn()
    };

    res = {
      redirect: jest.fn()
    };

    // Suppress console output in test logs
    jest.spyOn(console, "error").mockImplementation(() => {});
  });

  // Test Case 1: Missing required fields
  it("should redirect if any field is missing", async () => {
    req.body = { username: "", password: "", password2: "" };

    await RegisterAccountController.registerAccount(req as Request, res as Response);

    expect(req.flash).toHaveBeenCalledWith("error", "Please fill in all fields.");
    expect(res.redirect).toHaveBeenCalledWith("/register");
  });

  // Test Case 2: Passwords don't match
  it("should redirect if passwords do not match", async () => {
    req.body = { username: "testuser", password: "123", password2: "456" };

    await RegisterAccountController.registerAccount(req as Request, res as Response);

    expect(req.flash).toHaveBeenCalledWith("error", "Passwords do not match.");
    expect(res.redirect).toHaveBeenCalledWith("/register");
  });

  // Test Case 3: Successful registration
  it("should call API and redirect to /dashboard on success", async () => {
    // Mock successful registration response
    mockedAxios.post.mockResolvedValueOnce({
      data: {
        access_token: "new-token"
      },
      status: 201,
      statusText: "Created",
      headers: {},
      config: { url: "" }
    });

    await RegisterAccountController.registerAccount(req as Request, res as Response);

    // Ensure backend API was called with correct payload
    expect(mockedAxios.post).toHaveBeenCalledWith(
      expect.stringContaining("/auth/register"),
      {
        username: "testuser",
        password: "pass123"
      }
    );

    // Ensure session was set with user and token
    expect(req.session!.user).toEqual({
      username: "testuser",
      token: "new-token"
    });

    // Redirects to dashboard after registration
    expect(res.redirect).toHaveBeenCalledWith("/dashboard");
  });

  // Test Case 4: Known error from backend (e.g., user exists)
  it("should handle API errors and redirect to /login with message", async () => {
    mockedAxios.post.mockRejectedValueOnce({
      response: {
        data: {
          msg: "Username already exists"
        }
      }
    });

    await RegisterAccountController.registerAccount(req as Request, res as Response);

    expect(req.flash).toHaveBeenCalledWith("error", "Username already exists");
    expect(res.redirect).toHaveBeenCalledWith("/login");
  });

  // Test Case 5: Unknown or malformed error object
  it("should handle unknown errors gracefully", async () => {
    mockedAxios.post.mockRejectedValueOnce({}); // No response.data.msg

    await RegisterAccountController.registerAccount(req as Request, res as Response);

    expect(req.flash).toHaveBeenCalledWith("error", "Something went wrong. Please try again later.");
    expect(res.redirect).toHaveBeenCalledWith("/login");
  });
});
