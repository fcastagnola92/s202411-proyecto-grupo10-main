import api from "@Api/api";
import config from "@Config/index";
import { Logger } from "@Utils/logger";
import PostgresDatabase from "@Infrastructure/database/postgresDatabase";

const log = Logger(__filename);

const initializateDatabase = () => {
  const instance = PostgresDatabase.getInstance();
  if (instance.dataSource.isInitialized) {
    log.info("Database is initializated 🟢");
  }
};

const closeDatabase = async () => {
  const instance = PostgresDatabase.getInstance();
  await instance.close();
  if (!instance.dataSource.isInitialized) {
    log.info("Database was closed 🔴");
  }
};

const listener = api.listen(config.PORT, () => {
  initializateDatabase();
  log.info(
    `The service is running ✅ 🚀 on port ${config.PORT} in ${config.ENVIRONMENT} environment`
  );
});

const gracefulShutdown = () => {
  log.info("🔴 Received kill signal, shutting down gracefully.");
  listener.close(() => {
    log.info("Closed out remaining connections. 🔴");
    closeDatabase().then(() => {
      log.info("Database shutdown called");
    });
    process.exit(0);
  });
};

process.on("uncaughtException", (err) => {
  log.error("uncaughtException", err);
  process.exit(1);
});

process.on("SIGTERM", gracefulShutdown);

process.on("SIGINT", gracefulShutdown);
