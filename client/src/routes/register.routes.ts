import { Router } from "express";
import {RegisterAccountController} from "../controllers/register.controller";
import {inputValidation} from "../middleware/inputValidation.middleware";

const router = Router();

// results page
router.get("/register", async (req, res) => {

    res.render("register", {
    });
  }
);
// Handle POST request when the form submits
router.post("/register", inputValidation, RegisterAccountController.registerAccount);

export default router;
