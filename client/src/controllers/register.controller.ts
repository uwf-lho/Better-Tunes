import { Request, Response } from "express";
import axios from "axios";

const apiBaseUrl:string = process.env.API_BASE_URL || "http://localhost:8080";

export class RegisterAccountController {
  static async registerAccount(req: Request, res: Response): Promise<void> {

    try {
        // Extract form data correctly
        const username = req.body["username"];
        const password1 = req.body["password"];
        const password2 = req.body["password2"];

        if (!username || !password1 || !password2) {
            req.flash("error", "Please fill in all fields.");
            return res.redirect("/register");
        }

        if (password1 != password2) {
            req.flash("error", "Passwords do not match.");
            return res.redirect("/register");
        }

        // Call API with form data
        const response = await axios.post(`${apiBaseUrl}/auth/register`, {
            "username": username,
            "password": password1
        });

        const results: any = response.data;

        let token: any = results.access_token;

        req.session.user = {username: username, token: token};

        // Render dashboard after successfully registering
        res.redirect("/dashboard")

    } catch (error: any) {
        console.error("Register Error:", error);
        const flashMessage = error.response?.data?.msg || "Something went wrong. Please try again later.";

        req.flash("error", flashMessage);
        return res.redirect("/login"); // Stops execution in case of an error
    }
}

}