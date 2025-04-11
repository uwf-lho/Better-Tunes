import { Request, Response } from "express";
import axios from "axios";

const apiBaseUrl:string = process.env.API_BASE_URL || "http://localhost:8080";


export class SearchController {
  static async getResults(req: Request, res: Response): Promise<void> {

    try {
        // Extract form data correctly
        const search_query = req.body["search-input"]; // Correctly matches form input
        const category = req.body["query-type-dropdown"]; // Matches the dropdown name

        if (!search_query || !category) {
            req.flash("error", "Please fill in all fields.");
            return res.redirect("/dashboard");
        }

        // Call API with form data
        const response = await axios.post(`${apiBaseUrl}/api/search`, {
            query_type: category,
            payload: search_query,
            username: req.session.user?.username
        });

        const results = response.data;

        // Render results page with received data
        res.render("results", {
            user: req.session?.user, // Prevents crashes if session is undefined
            cards: results,
            query_type: category,  // TODO change this to be queryType
            search_query: search_query,
            userId: req.session.user?.username
        });

    } catch (error: any) {
        console.error("Search Error:", error);
        const flashMessage = error.response?.data?.msg || "Something went wrong. Please try again later.";

        req.flash("error", flashMessage);
        return res.redirect("/login"); // Stops execution in case of an error
    }
}

}