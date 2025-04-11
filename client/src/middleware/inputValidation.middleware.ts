import { Request, Response, NextFunction } from "express";

export function inputValidation(req: Request, res: Response, next: NextFunction) {
  const { username, password } = req.body;
  const referer = req.get("referer") || "/"; // fallback to home if referer is missing

  if (!username || typeof username !== "string" || username.trim().length < 3) {
    req.flash("error", "Username must be at least 3 characters long.");
    return res.redirect(referer);
  }

  if (!password || typeof password !== "string") {
    req.flash("error", "Password is required.");
    return res.redirect(referer);
  }

  // If on the registration page, enforce minimum password length
  if (referer.includes("register") && password.trim().length < 6) {
    req.flash("error", "Password must be at least 6 characters.");
    return res.redirect(referer);
  }

  next(); // All good, move on
}