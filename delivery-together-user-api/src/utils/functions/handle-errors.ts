import { Response } from "express";
import { StatusCodes } from "http-status-codes";

export const notFoundError = (_res: Response): Response<void> => {
    return _res.status(StatusCodes.NOT_FOUND).send()
};

export const unprocessableError = (_res: Response): Response<void> => {
    return _res.status(StatusCodes.UNPROCESSABLE_ENTITY).send()
};

export const badRequestError = (_res: Response): Response<void> => {
    return _res.status(StatusCodes.BAD_REQUEST).send()
};

export const unauthorizedError = (_res: Response): Response<void> => {
    return _res.status(StatusCodes.UNAUTHORIZED).send()
};

export const internalServerError = (_res: Response): Response<void> => {
    return _res.status(StatusCodes.INTERNAL_SERVER_ERROR)
};

export const preconditionFailed = (_res: Response): Response<void> => {
    return _res.status(StatusCodes.PRECONDITION_FAILED).send()
};

export const forbiddeError = (_res: Response): Response<void> => {
    return _res.status(StatusCodes.FORBIDDEN).send()
};