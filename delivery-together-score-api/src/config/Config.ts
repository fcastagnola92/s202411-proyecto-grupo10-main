type Database = {
  USER?: string,
  PASSWORD?: string,
  HOST?: string,
  PORT?: string,
  NAME?: string
}
interface Config {
    APP_ENV: string | undefined,
    ENVIRONMENT: string | undefined;
    PORT: string | undefined;
    USERS_PATH: string | undefined;
    DATABASE: Database
  }
  
  export default Config;