import { DataSource } from "typeorm";
import Database from "@Infrastructure/database/Database";
import config from "@Config/index";
import { Logger } from "@Utils/logger";
import Score from "./entities/Score";

const log = Logger(__filename);

class PostgresDatabase implements Database {
  private static instance: PostgresDatabase | null = null;
  dataSource: DataSource;

  private constructor() {
    this.dataSource = new DataSource({
      type: "postgres",
      host: config.DATABASE.HOST,
      port: parseInt(config.DATABASE.PORT, 10),
      username: config.DATABASE.USER,
      password: config.DATABASE.PASSWORD,
      database: config.DATABASE.NAME,
      entities: [Score],
      synchronize: true
    });
  }

  static getInstance(): PostgresDatabase {
    if (!PostgresDatabase.instance) {
        PostgresDatabase.instance = new PostgresDatabase();
        PostgresDatabase.instance.connection().then(connected => {
          if (connected) {
            log.info('Database connected 🟢');
          }
          else {
            log.error('Some error ocurred in database connection');
          }
        }).catch((err) => {
          console.log(err);
          log.error('Some error ocurred in database connection');
        });
    }
    return PostgresDatabase.instance;
  }

  context(): DataSource {
    return this.dataSource;
  }
  async connection() {
    try {
      const connection = await this.dataSource.initialize();
      return connection.isInitialized;
    } catch (ex) {
      if (ex instanceof Error) {
        log.error("Some error ocurred trying to make", {
          errorMessage: ex.message,
          stack: ex.stack,
        });
        throw ex;
      }
    }
  }
  async close() {
    if (this.dataSource.initialize) {
      await this.dataSource.destroy();
    }
  }
}

export default PostgresDatabase;
