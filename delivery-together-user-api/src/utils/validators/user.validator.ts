import { check } from "express-validator";
import { validateFields } from "../../middlewares/validate-fields";

export const createUserCheck = () => {
    return [
        check("password").exists(),////no esté presente en la solicitud
        check("password").notEmpty(),//no correspondan a lo esperado.
        check("username").exists(),////no esté presente en la solicitud
        check("username").notEmpty(),//no correspondan a lo esperado.
        check("email").exists(),////no esté presente en la solicitud
        check("email").isEmail(),//no correspondan a lo esperado.
        check("email").notEmpty(),//no correspondan a lo esperado.
        validateFields,

    ]
}

