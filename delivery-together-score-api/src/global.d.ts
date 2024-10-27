import type Context from "@Infrastructure/middleware/Context";

declare global {
  namespace Express {
    interface Request {
      context: Context;
    }
  }
}
