import { Request, Response, NextFunction } from 'express';
import { Logger } from "@Utils/logger";

const log = Logger(__filename);

const PreRequest = (req: Request, res: Response, next: NextFunction) => {
    res.setHeader('Content-Type', 'application/json');
    log.info("Initialization request", { method: req.method, url: req.url  });
    
    next();
};

export default PreRequest;