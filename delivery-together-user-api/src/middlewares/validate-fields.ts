import { Request, Response } from "express";
import { StatusCodes } from 'http-status-codes';
import { validationResult } from "express-validator";

export const validateFields = (_req: Request, _res: Response, next: Function): void | Response => {
    const errors = validationResult(_req);

    if (!errors.isEmpty()) return _res.status(StatusCodes.BAD_REQUEST).json();

    next();
}