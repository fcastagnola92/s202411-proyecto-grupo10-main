import Express from "express";
import Ping from "@Application/ping";
import Score from "@Infrastructure/inputs/score";
import ValidateAuthentication from "@Infrastructure/middleware/auth";

const router = Express.Router();

router.get("/scores/ping", Ping);

router.post("/scores", ValidateAuthentication, Score);

export default router;
