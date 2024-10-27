import { Request, Response } from "express";
import { unauthorizedError } from "../utils/functions/handle-errors";
import { User } from "../entities/User";


export const Auth = async (_req: Request, _res: Response, next: Function): Promise<void | Response> => {
    try {

        if (!_req.header('Authorization')) {
            return unauthorizedError(_res);
        }

        const token = _req.header('Authorization')?.replace('Bearer ', '');
        const timeNow = new Date();
        timeNow.setMinutes(timeNow.getMinutes());
        // leer el usuario que corresponde al uid
        const user: User | null = await User.findOneBy({ token });

        if (!user || timeNow.toISOString() > user.expireAt) {
            return unauthorizedError(_res);
        }
        (_req).body.user = user;

        next();

    } catch (error) {
        return unauthorizedError(_res);
    }
};