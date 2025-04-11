import { Router } from "express";
import { ensureAuthenticated } from "../middleware/ensureAuthenticated.middleware";

const router = Router();

router.get("/about", async (req, res) => {
    res.render("about", {
    });
  }
);


export default router;
