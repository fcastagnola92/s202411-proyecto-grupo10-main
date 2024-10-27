import * as dotenv from "dotenv";
import Config from "./Config";

dotenv.config();

process.env.APP_ENV = process.env.APP_ENV || "development";
process.env.NODE_ENV = process.env.NODE_ENV || "development";

const config: Config = {
  APP_ENV: process.env.APP_ENV,
  ENVIRONMENT: process.env.NODE_ENV,
  PORT: process.env.PORT || "3004",
  USERS_PATH: process.env.USERS_PATH || "",
  DATABASE: {
    USER: process.env.DB_USER,
    PASSWORD: process.env.DB_PASSWORD,
    HOST: process.env.DB_HOST,
    PORT: process.env.DB_PORT,
    NAME: process.env.DB_NAME,
  },
};

export default config;
