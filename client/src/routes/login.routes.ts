import { Router } from "express";
import {LoginAccountController} from "../controllers/login.controller";
import {inputValidation} from "../middleware/inputValidation.middleware";

const router = Router();

// login page
router.get("/login", async (req, res) => {

    res.render("login", {
    });
  }
);
// Handle POST request when the form submits
router.post("/login", inputValidation, LoginAccountController.loginAccount);


export default router;
