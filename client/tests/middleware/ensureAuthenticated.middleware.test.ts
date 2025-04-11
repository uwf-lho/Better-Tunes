import { Request, Response, NextFunction } from "express";
import { ensureAuthenticated } from "../../src/middleware/ensureAuthenticated.middleware";

describe("ensureAuthenticated middleware", () => {
  let req: Partial<Request>;
  let res: Partial<Response>;
  let next: NextFunction;

  beforeEach(() => {
    // Default to no user in session
    req = {
      session: { user: undefined } as any,
      flash: jest.fn() // Mock flash messaging
    };

    res = {
      redirect: jest.fn() // Mock redirect
    };

    next = jest.fn(); // Mock next function
  });

  // Test Case 1: User is authenticated — allow request
  it("should allow request to proceed if user is authenticated", () => {
    req.session = { user: { username: "testuser", token: "abc123" } } as any;

    ensureAuthenticated(req as Request, res as Response, next);

    expect(next).toHaveBeenCalled();               // Proceed to next middleware
    expect(res.redirect).not.toHaveBeenCalled();   // No redirect
    expect(req.flash).not.toHaveBeenCalled();      // No flash message
  });

  // Test Case 2: Session exists, but user is not present
  it("should redirect and flash error if user is not authenticated", () => {
    req.session = {} as any; // No user in session

    ensureAuthenticated(req as Request, res as Response, next);

    expect(req.flash).toHaveBeenCalledWith(
      "error",
      "Please be logged in to access internal pages."
    );
    expect(res.redirect).toHaveBeenCalledWith("/"); // Redirect to landing page
    expect(next).not.toHaveBeenCalled();            // Do not proceed
  });

  // Test Case 3: Session object is missing entirely
  it("should redirect and flash error if session is missing", () => {
    req.session = undefined;

    ensureAuthenticated(req as Request, res as Response, next);

    expect(req.flash).toHaveBeenCalledWith(
      "error",
      "Please be logged in to access internal pages."
    );
    expect(res.redirect).toHaveBeenCalledWith("/"); // Redirect to landing page
    expect(next).not.toHaveBeenCalled();            // Do not proceed
  });
});
