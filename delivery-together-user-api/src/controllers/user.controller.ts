import { Request, Response } from "express";
import * as userServices from "../services/user.service";

export const ping = (_req: Request, _res: Response): Promise<Response> => {
    return userServices.ping(_req, _res);
};

export const create = (_req: Request, _res: Response): Promise<Response> => {
    return userServices.create(_req.body, _res)
};

export const token = (_req: Request, _res: Response): Promise<Response> => {
    return userServices.token(_req.body, _res)
};

export const get = (_req: Request, _res: Response): Promise<Response> => {
    return userServices.get(_req.body, _res)
};

export const update = (_req: Request, _res: Response): Promise<Response> => {
    return userServices.update(_req.params.id, _req.body, _res)
}

export const hook = (_req: Request, _res: Response): Promise<Response> => {
    return userServices.hook(_req.body, _res)
}

export const reset = (_req: Request, _res: Response): Promise<Response> => {
    return userServices.reset(_res)
}