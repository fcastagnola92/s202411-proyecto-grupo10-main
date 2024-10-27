import { check } from "express-validator";
import { validateFields } from "../../middlewares/validate-fields";
import { Status } from "../enums/status.enum";

export const updateUserCheck = () => {
    return [
        check("status").exists(),////no esté presente en la solicitud
        check("status").notEmpty(),//no correspondan a lo esperado.
        check("status").custom(isStatusValid),
        validateFields,

    ]
}

const isStatusValid = (status: string): Promise<void> => {

    const existRole = Object.values(Status).includes(status as Status)
    if (!existRole) {
        throw new Error();
    }
    return Promise.resolve();
}