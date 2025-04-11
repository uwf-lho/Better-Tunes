import { Router } from "express";
import { ensureAuthenticated } from "../middleware/ensureAuthenticated.middleware";
import { SearchController } from "../controllers/search.controller";

const router = Router();

// results page
router.get("/results", SearchController.getResults);

// Handle POST request when the form submits
router.post("/results", SearchController.getResults);

export default router;
