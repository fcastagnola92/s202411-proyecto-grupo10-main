import { check } from "express-validator";
import { validateFields } from "../../middlewares/validate-fields";

export const authCheck = () => {
    return [
        check("password").exists(),////no esté presente en la solicitud
        check("password").notEmpty(),//no correspondan a lo esperado.
        check("username").exists(),////no esté presente en la solicitud
        check("username").notEmpty(),
        validateFields,

    ]
}

