import { Router } from "express";
import { ReactionHandler } from "../controllers/reaction.controller";

const router = Router();

// POST /react
router.post("/react", ReactionHandler.handleReaction);

export default router;