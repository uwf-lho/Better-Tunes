import { Request, Response, NextFunction } from "express";

export function ensureAuthenticated(req: Request, res: Response, next: NextFunction) {
  if (!req.session || !req.session.user) {
    req.flash("error", "Please be logged in to access internal pages.");
    return res.redirect("/"); // Redirect to the login page
  }
  next(); // Proceed to the next middleware/route handler
}
