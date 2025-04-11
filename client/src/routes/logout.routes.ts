import { Router } from "express";
import {LoginAccountController} from "../controllers/login.controller";

const router = Router();

router.get("/logout", async (req, res) => {
  req.session.user = undefined;
  req.flash("success", "Successfully logged out.");
  res.redirect("/");
});

export default router;
