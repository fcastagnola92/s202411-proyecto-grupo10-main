import { Router } from "express";
import { Auth } from "../middlewares/auth";
import { authCheck } from "../utils/validators/auth.validator";
import { createUserCheck } from "../utils/validators/user.validator"
import { updateUserCheck } from "../utils/validators/update-user.validator";
import { create, ping, token, get, update, reset, hook } from "../controllers/user.controller";


const router = Router()

router.get("/ping", ping);

router.post("/",
    createUserCheck(),
    create
)
router.post("/auth",
    authCheck(),
    token)

router.get("/me", [Auth],
    get)

router.patch("/:id",
    updateUserCheck(),
    update)

router.post("/reset",
    reset)

router.patch("/hook/update",
    hook)

export default router;