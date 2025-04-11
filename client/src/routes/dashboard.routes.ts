import { Router } from "express";
import {ensureAuthenticated} from "../middleware/ensureAuthenticated.middleware";


const router = Router();

router.get("/dashboard", ensureAuthenticated, async (req, res) => {

    res.render("dashboard", {
    });
  }
);


export default router;
