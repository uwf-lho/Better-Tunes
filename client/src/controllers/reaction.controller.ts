import { Request, Response } from "express";
import axios from "axios";

const apiBaseUrl:string = process.env.API_BASE_URL || "http://localhost:8080";

export class ReactionHandler {
  static async handleReaction(req: Request, res: Response): Promise<void> {
    try {
        const { songId, action, userId } = req.body;

        if (!songId || !action || !userId) {
            res.status(400).json({ error: "Missing data" });  // maybe we should handle this better
            return;
        }

        const response = await axios.post(`${apiBaseUrl}/api/update-song`, {
            "songId": songId,
            "action": action,
            "userId": userId
        });

        res.status(200).json({ success: "Successfully updated song" });
        return;

    } catch (error: any) {
        console.error("User Reaction Error:", error);
        res.status(400).json({ error: error });
        return; // Stops execution in case of an error
    }
  }
}
