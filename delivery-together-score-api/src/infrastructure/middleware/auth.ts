import { Request, Response, NextFunction } from "express";
import { StatusCodes } from "http-status-codes";
import { Logger } from "@Utils/logger";
import AuthApplication from "@Application/auth";
import UserHttpRepository from "@Infrastructure/repository/httpClient/UserHttpRepository";
import type Context from "./Context";

const log = Logger(__filename);

const ValidateAuthentication = async (
  req: Request,
  res: Response,
  next: NextFunction
) => {
  const authHeader = req.headers.authorization;
  const authApplication = new AuthApplication(new UserHttpRepository());
  if (authHeader == "" || !authHeader) {
    log.error("Forbidden user");
    res.status(StatusCodes.FORBIDDEN).end();
    return;
  }

  if (!authHeader.includes("Bearer")) {
    log.error("Invalid Authorization header");
    res.status(StatusCodes.UNAUTHORIZED).end();
    return;
  }

  const token = authHeader.split(" ")[1];

  log.info("Received token", {
    token,
  });
  try {
    const user = await authApplication.tokenValidator(token);

    if (user) {
      const context: Context = {
        userId: user.id,
      };
      req.context = context;
      res.status(StatusCodes.OK);
      next();
    } else {
      res.status(StatusCodes.UNAUTHORIZED).end();
    }
  } catch (ex) {
    if (ex instanceof Error) {
      log.error("Unauthorized", {
        errorMessage: ex.message,
        stack: ex.stack,
      });
      res.status(StatusCodes.UNAUTHORIZED).end();
    }

    return;
  }
};

export default ValidateAuthentication;
