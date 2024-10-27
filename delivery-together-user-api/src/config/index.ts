import * as dotenv from 'dotenv';

dotenv.config();

enum NodeEnv {
  TEST = 'test',
  DEV = 'development',
}

interface Env {
  env: NodeEnv;
  dbName: string;
  dbTestName: string;
  dbPassword: string;
  port: number;
  dbUserName: string;
  dbHost: string;
  secretKet: string;
  trueNativeHost: string;
  trueNativePort: number
  trueNativePath: string;
  trueNativeUserWebHook: string;
  secretToken: string
  mailHost: string;
  mailPort: number;
  mailPath: string
}


console.log(process.env)

export const config: Env = {
  env: (process.env.NODE_ENV as NodeEnv) || NodeEnv.TEST,
  dbName: process.env.DB_NAME || '',
  dbTestName: process.env.DB_TEST_NAME || '',
  port: process.env.APP_PORT ? parseInt(process.env.APP_PORT, 10) : 8000,
  dbUserName: process.env.DB_USER || '',
  dbPassword: process.env.DB_PASSWORD || '',
  dbHost: process.env.DB_HOST || '',
  secretKet: process.env.SECRET_KEY || '',
  trueNativeHost: process.env.TRUE_NATIVE_HOST || '',
  trueNativePort: process.env.TRUE_NATIVE_PORT ? parseInt(process.env.TRUE_NATIVE_PORT, 10) : 3000,
  trueNativePath: process.env.TRUE_NATIVE_PATH || '',
  trueNativeUserWebHook: process.env.TRUE_NATIVE_USER_WEBHOOK || '',
  secretToken: process.env.SECRET_TOKEN || '',
  mailHost: process.env.MAIL_HOST || '',
  mailPort: process.env.MAIL_PORT ? parseInt(process.env.MAIL_PORT, 10) : 3006,
  mailPath: process.env.MAIL_PATH || '',
};