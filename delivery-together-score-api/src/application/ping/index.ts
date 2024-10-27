import { Request, Response } from "express";
import { StatusCodes } from "http-status-codes";
import { Logger } from "@Utils/logger";

const log = Logger(__filename);

const Ping = async (_request: Request, response: Response) => {
  try {
    const status = StatusCodes.OK;

    response.setHeader("Content-Type", "text/plain");
    const data: string = "pong";

    response.status(status).send(data);
  } catch (error: any) {
    log.error("Error in Health Route", {
      errorMessage: error.message,
      stack: error.stack,
    });
    const status = StatusCodes.INTERNAL_SERVER_ERROR;
    response.status(status);
  }
};


export default Ping