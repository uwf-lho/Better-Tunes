import { Request, Response } from "express";
import axios from "axios";

const apiBaseUrl:string = process.env.API_BASE_URL || "http://localhost:8080";

export class LoginAccountController {
  static async loginAccount(req: Request, res: Response): Promise<void> {
    try {
        // Extract form data correctly
        const username = req.body["username"];
        const password1 = req.body["password"];

        if (!username || !password1) {
            req.flash("error", "Please fill in all fields.");
            return res.redirect("/login"); // Stops execution
        }

        // Call API with form data
        const response = await axios.post(`${apiBaseUrl}/auth/login`, {
            "username": username,
            "password": password1
        });

        const results: any = response.data;

        // Store session details
        req.session.user = { username: username, token: results.access_token };

        // Redirect to dashboard after successful login
        return res.redirect("/dashboard");

    } catch (error: any) {
        console.error("Login Error:", error);
        const flashMessage = error.response?.data?.msg || "Something went wrong. Please try again later.";

        req.flash("error", flashMessage);
        return res.redirect("/login"); // Stops execution in case of an error
    }
  }
}
